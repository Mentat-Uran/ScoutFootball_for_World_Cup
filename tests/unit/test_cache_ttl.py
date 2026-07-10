"""Tests for the _TTLCache class and TTL-cached data-loader functions.

Covers:
- _TTLCache get/set/invalidate basics
- TTL expiration (via mocked time and short TTL)
- Environment variable configuration (SCOUTFOOTBALL_CACHE_TTL_SECONDS)
- force_refresh bypasses the cache
- Cache hit avoids re-reading Parquet
"""

from __future__ import annotations

import os
import time
from unittest.mock import patch

import pandas as pd
import pytest

from scoutfootball.app.data_loader import (
    _MISSING,
    _load_all_player_ratings,
    _ttl_cache,
    _TTLCache,
)

# ---------------------------------------------------------------------------
# 1. _TTLCache unit tests
# ---------------------------------------------------------------------------


class TestTTLCacheBasics:
    """Basic get/set/invalidate behavior."""

    def test_get_missing_key_returns_missing(self) -> None:
        cache = _TTLCache()
        assert cache.get("nonexistent") is _MISSING

    def test_set_then_get_returns_value(self) -> None:
        cache = _TTLCache()
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_set_overwrites_previous_value(self) -> None:
        cache = _TTLCache()
        cache.set("key1", "old")
        cache.set("key1", "new")
        assert cache.get("key1") == "new"

    def test_invalidate_removes_entry(self) -> None:
        cache = _TTLCache()
        cache.set("key1", "value1")
        cache.invalidate("key1")
        assert cache.get("key1") is _MISSING

    def test_invalidate_nonexistent_key_is_noop(self) -> None:
        cache = _TTLCache()
        cache.invalidate("never_set")  # should not raise

    def test_cache_stores_various_types(self) -> None:
        cache = _TTLCache()
        cache.set("df", pd.DataFrame({"a": [1, 2]}))
        cache.set("list", [1, 2, 3])
        cache.set("none", None)
        assert isinstance(cache.get("df"), pd.DataFrame)
        assert cache.get("list") == [1, 2, 3]
        # None is a valid cached value — must not be confused with _MISSING
        assert cache.get("none") is None
        assert cache.get("none") is not _MISSING


# ---------------------------------------------------------------------------
# 2. TTL expiration
# ---------------------------------------------------------------------------


class TestTTLExpiration:
    """Values expire after the configured TTL."""

    def test_expired_entry_returns_missing(self) -> None:
        cache = _TTLCache()
        cache._ttl = 0.1  # 100ms
        cache.set("ephemeral", "gone_soon")
        assert cache.get("ephemeral") == "gone_soon"
        time.sleep(0.15)
        assert cache.get("ephemeral") is _MISSING

    def test_non_expired_entry_still_valid(self) -> None:
        cache = _TTLCache()
        cache._ttl = 10.0
        cache.set("stable", "value")
        assert cache.get("stable") == "value"

    def test_expiration_uses_time_time(self) -> None:
        """Mock time.time to simulate expiration without sleeping."""
        cache = _TTLCache()
        cache._ttl = 300.0

        # Simulate: set at t=1000, get at t=1000 (fresh)
        with patch("scoutfootball.app.data_loader.time.time", return_value=1000.0):
            cache.set("key", "val")
        with patch("scoutfootball.app.data_loader.time.time", return_value=1000.0):
            assert cache.get("key") == "val"

        # Simulate: get at t=1400 (expired, 400 > 300)
        with patch("scoutfootball.app.data_loader.time.time", return_value=1400.0):
            assert cache.get("key") is _MISSING

    def test_entry_just_within_ttl(self) -> None:
        cache = _TTLCache()
        cache._ttl = 300.0

        with patch("scoutfootball.app.data_loader.time.time", return_value=1000.0):
            cache.set("key", "val")
        # 300 seconds later: exactly at TTL boundary (300 > 300 is False → still fresh)
        with patch("scoutfootball.app.data_loader.time.time", return_value=1300.0):
            assert cache.get("key") == "val"
        # 301 seconds later: expired
        with patch("scoutfootball.app.data_loader.time.time", return_value=1301.0):
            assert cache.get("key") is _MISSING


# ---------------------------------------------------------------------------
# 3. Environment variable configuration
# ---------------------------------------------------------------------------


class TestTTLCacheEnvConfig:
    """SCOUTFOOTBALL_CACHE_TTL_SECONDS controls the TTL at instantiation."""

    def test_env_var_sets_custom_ttl(self) -> None:
        with patch.dict(os.environ, {"SCOUTFOOTBALL_CACHE_TTL_SECONDS": "1"}):
            cache = _TTLCache()
        assert cache._ttl == 1.0

    def test_env_var_sets_large_ttl(self) -> None:
        with patch.dict(os.environ, {"SCOUTFOOTBALL_CACHE_TTL_SECONDS": "600"}):
            cache = _TTLCache()
        assert cache._ttl == 600.0

    def test_env_var_zero_falls_back_to_default(self) -> None:
        with patch.dict(os.environ, {"SCOUTFOOTBALL_CACHE_TTL_SECONDS": "0"}):
            cache = _TTLCache()
        assert cache._ttl == _TTLCache._DEFAULT_TTL

    def test_env_var_negative_falls_back_to_default(self) -> None:
        with patch.dict(os.environ, {"SCOUTFOOTBALL_CACHE_TTL_SECONDS": "-5"}):
            cache = _TTLCache()
        assert cache._ttl == _TTLCache._DEFAULT_TTL

    def test_env_var_non_numeric_falls_back_to_default(self) -> None:
        with patch.dict(os.environ, {"SCOUTFOOTBALL_CACHE_TTL_SECONDS": "abc"}):
            cache = _TTLCache()
        assert cache._ttl == _TTLCache._DEFAULT_TTL

    def test_env_var_unset_uses_default(self) -> None:
        env = {k: v for k, v in os.environ.items() if k != "SCOUTFOOTBALL_CACHE_TTL_SECONDS"}
        with patch.dict(os.environ, env, clear=True):
            cache = _TTLCache()
        assert cache._ttl == _TTLCache._DEFAULT_TTL

    def test_short_ttl_from_env_expires_quickly(self) -> None:
        """Integration: a real short TTL from env causes expiration."""
        with patch.dict(os.environ, {"SCOUTFOOTBALL_CACHE_TTL_SECONDS": "0.1"}):
            cache = _TTLCache()
        assert cache._ttl == 0.1
        cache.set("k", "v")
        assert cache.get("k") == "v"
        time.sleep(0.15)
        assert cache.get("k") is _MISSING


# ---------------------------------------------------------------------------
# 4. force_refresh bypasses cache
# ---------------------------------------------------------------------------


@pytest.fixture
def _clean_ratings_cache():
    """Ensure the module-level _ttl_cache has no stale '_load_all_player_ratings' entry."""
    cache_key = "_load_all_player_ratings"
    _ttl_cache.invalidate(cache_key)
    yield
    _ttl_cache.invalidate(cache_key)


class TestForceRefresh:
    """force_refresh=True bypasses the TTL cache and reloads from source."""

    def test_force_refresh_returns_new_data_after_change(
        self, _clean_ratings_cache: None,
    ) -> None:
        df_v1 = pd.DataFrame(
            {"player": ["Alpha"], "optimized_score": [50.0]},
        )
        df_v2 = pd.DataFrame(
            {"player": ["Beta"], "optimized_score": [90.0]},
        )

        with patch("scoutfootball.app.data_loader._duckdb_exists", return_value=False):
            # First load — caches df_v1
            with patch(
                "scoutfootball.app.data_loader._safe_read_parquet",
                return_value=df_v1.copy(),
            ):
                result1 = _load_all_player_ratings()
            assert "Alpha" in result1["player"].values

            # Second load without force_refresh — should return cached df_v1
            with patch(
                "scoutfootball.app.data_loader._safe_read_parquet",
                return_value=df_v2.copy(),
            ):
                result2 = _load_all_player_ratings()
            assert "Alpha" in result2["player"].values
            assert "Beta" not in result2["player"].values

            # Third load with force_refresh — should reload df_v2
            with patch(
                "scoutfootball.app.data_loader._safe_read_parquet",
                return_value=df_v2.copy(),
            ):
                result3 = _load_all_player_ratings(force_refresh=True)
            assert "Beta" in result3["player"].values

    def test_force_refresh_true_bypasses_even_fresh_cache(
        self, _clean_ratings_cache: None,
    ) -> None:
        df = pd.DataFrame({"player": ["Gamma"], "optimized_score": [60.0]})

        with patch("scoutfootball.app.data_loader._duckdb_exists", return_value=False):
            with patch(
                "scoutfootball.app.data_loader._safe_read_parquet",
                return_value=df.copy(),
            ) as mock_read:
                _load_all_player_ratings()
                initial_calls = mock_read.call_count

                # force_refresh should re-invoke _safe_read_parquet
                _load_all_player_ratings(force_refresh=True)
                assert mock_read.call_count > initial_calls


# ---------------------------------------------------------------------------
# 5. Cache hit avoids re-reading Parquet
# ---------------------------------------------------------------------------


class TestCacheHit:
    """Within TTL, repeated calls return cached data without re-reading Parquet."""

    def test_cache_hit_skips_parquet_read(
        self, _clean_ratings_cache: None,
    ) -> None:
        df = pd.DataFrame({"player": ["Delta"], "optimized_score": [55.0]})

        with patch("scoutfootball.app.data_loader._duckdb_exists", return_value=False):
            with patch(
                "scoutfootball.app.data_loader._safe_read_parquet",
                return_value=df.copy(),
            ) as mock_read:
                _load_all_player_ratings()
                calls_after_first = mock_read.call_count

                # Second call within TTL — should not read parquet again
                _load_all_player_ratings()
                assert mock_read.call_count == calls_after_first

    def test_cache_hit_returns_same_object(
        self, _clean_ratings_cache: None,
    ) -> None:
        """Within TTL, the exact same cached DataFrame object is returned."""
        df = pd.DataFrame({"player": ["Epsilon"], "optimized_score": [70.0]})

        with patch("scoutfootball.app.data_loader._duckdb_exists", return_value=False):
            with patch(
                "scoutfootball.app.data_loader._safe_read_parquet",
                return_value=df,
            ):
                result1 = _load_all_player_ratings()
                result2 = _load_all_player_ratings()
                # Same object reference (cached)
                assert result1 is result2

    def test_cache_miss_then_hit_then_invalidate_then_miss(
        self, _clean_ratings_cache: None,
    ) -> None:
        df = pd.DataFrame({"player": ["Zeta"], "optimized_score": [65.0]})

        with patch("scoutfootball.app.data_loader._duckdb_exists", return_value=False):
            with patch(
                "scoutfootball.app.data_loader._safe_read_parquet",
                return_value=df.copy(),
            ) as mock_read:
                # Miss — reads parquet
                _load_all_player_ratings()
                assert mock_read.call_count == 1

                # Hit — no new read
                _load_all_player_ratings()
                assert mock_read.call_count == 1

                # Invalidate — next call is a miss
                _ttl_cache.invalidate("_load_all_player_ratings")
                _load_all_player_ratings()
                assert mock_read.call_count == 2


# ---------------------------------------------------------------------------
# 6. load_model_meta / load_league_metrics / load_player_value_metrics cache behavior
# ---------------------------------------------------------------------------


class TestOtherCachedLoaders:
    """The other TTL-cached loaders also cache and respect force_refresh."""

    def test_load_model_meta_caches(self) -> None:
        from scoutfootball.app.data_loader import load_model_meta

        cache_key = "load_model_meta"
        _ttl_cache.invalidate(cache_key)
        try:
            with patch("scoutfootball.app.data_loader._duckdb_exists", return_value=False):
                with patch(
                    "scoutfootball.app.data_loader._parquet_path",
                    return_value=__import__("pathlib").Path(
                        "/nonexistent/optimized_params_meta.json",
                    ),
                ):
                    # JSON path doesn't exist → returns empty DataFrame, cached
                    result1 = load_model_meta()
                    result2 = load_model_meta()
                    # Cached — same object reference
                    assert result1 is result2
        finally:
            _ttl_cache.invalidate(cache_key)

    def test_load_player_value_metrics_force_refresh(self) -> None:
        from scoutfootball.app.data_loader import load_player_value_metrics

        cache_key = "load_player_value_metrics"
        _ttl_cache.invalidate(cache_key)
        try:
            df_v1 = pd.DataFrame({"player_name": ["A"], "xT_per_90": [0.1]})
            df_v2 = pd.DataFrame({"player_name": ["B"], "xT_per_90": [0.2]})

            with patch(
                "scoutfootball.app.data_loader._safe_read_parquet",
                return_value=df_v1.copy(),
            ):
                result1 = load_player_value_metrics()
            assert "A" in result1["player_name"].values

            # Without force_refresh — cached v1
            with patch(
                "scoutfootball.app.data_loader._safe_read_parquet",
                return_value=df_v2.copy(),
            ):
                result2 = load_player_value_metrics()
            assert "A" in result2["player_name"].values

            # With force_refresh — loads v2
            with patch(
                "scoutfootball.app.data_loader._safe_read_parquet",
                return_value=df_v2.copy(),
            ):
                result3 = load_player_value_metrics(force_refresh=True)
            assert "B" in result3["player_name"].values
        finally:
            _ttl_cache.invalidate(cache_key)
