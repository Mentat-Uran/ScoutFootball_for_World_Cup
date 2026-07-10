"""Tests for the TTL-cache migration of load_player_rolling and load_team_rolling.

Verifies that both loaders:
- Return DataFrames
- Cache their result in the module-level _ttl_cache on first call
- Return the cached value on a second call (no re-read)
- Honor force_refresh=True to bypass the cache
- Are NOT decorated with functools.lru_cache (no cache_info attribute)
"""

from __future__ import annotations

from unittest.mock import patch

import pandas as pd
import pytest

from scoutfootball.app.data_loader import (
    _MISSING,
    _ttl_cache,
    load_player_rolling,
    load_team_rolling,
)

_PLAYER_KEY = "load_player_rolling"
_TEAM_KEY = "load_team_rolling"


@pytest.fixture
def _clean_rolling_cache() -> None:
    """Ensure the module-level _ttl_cache has no stale rolling entries."""
    _ttl_cache.invalidate(_PLAYER_KEY)
    _ttl_cache.invalidate(_TEAM_KEY)
    yield
    _ttl_cache.invalidate(_PLAYER_KEY)
    _ttl_cache.invalidate(_TEAM_KEY)


# ---------------------------------------------------------------------------
# Returns DataFrames
# ---------------------------------------------------------------------------


class TestRollingLoadersReturnDataFrames:
    """Both loaders return pandas DataFrames."""

    def test_load_player_rolling_returns_dataframe(
        self, _clean_rolling_cache: None,
    ) -> None:
        df = load_player_rolling()
        assert isinstance(df, pd.DataFrame)

    def test_load_team_rolling_returns_dataframe(
        self, _clean_rolling_cache: None,
    ) -> None:
        df = load_team_rolling()
        assert isinstance(df, pd.DataFrame)


# ---------------------------------------------------------------------------
# Caching behavior
# ---------------------------------------------------------------------------


class TestRollingCacheBehavior:
    """Within TTL, repeated calls return the cached value without re-reading."""

    def test_player_rolling_caches_in_ttl_store(
        self, _clean_rolling_cache: None,
    ) -> None:
        df1 = load_player_rolling()
        assert _PLAYER_KEY in _ttl_cache._store
        df2 = load_player_rolling()
        # Cached — same object reference
        assert df1 is df2

    def test_team_rolling_caches_in_ttl_store(
        self, _clean_rolling_cache: None,
    ) -> None:
        df1 = load_team_rolling()
        assert _TEAM_KEY in _ttl_cache._store
        df2 = load_team_rolling()
        assert df1 is df2

    def test_player_rolling_cache_hit_skips_parquet_read(
        self, _clean_rolling_cache: None,
    ) -> None:
        with patch(
            "scoutfootball.app.data_loader._safe_read_parquet",
        ) as mock_read:
            # First call reads from source (real parquet or synthetic fallback);
            # only count calls that actually hit _safe_read_parquet.
            load_player_rolling()
            calls_after_first = mock_read.call_count

            # Second call within TTL — should not re-read
            load_player_rolling()
            assert mock_read.call_count == calls_after_first

    def test_team_rolling_cache_hit_skips_parquet_read(
        self, _clean_rolling_cache: None,
    ) -> None:
        with patch(
            "scoutfootball.app.data_loader._safe_read_parquet",
        ) as mock_read:
            load_team_rolling()
            calls_after_first = mock_read.call_count

            load_team_rolling()
            assert mock_read.call_count == calls_after_first


# ---------------------------------------------------------------------------
# force_refresh
# ---------------------------------------------------------------------------


class TestRollingForceRefresh:
    """force_refresh=True bypasses the TTL cache and re-reads."""

    def test_player_rolling_force_refresh_re_reads(
        self, _clean_rolling_cache: None,
    ) -> None:
        with patch(
            "scoutfootball.app.data_loader._safe_read_parquet",
        ) as mock_read:
            load_player_rolling()
            calls_after_first = mock_read.call_count

            # Without force_refresh — cached, no new read
            load_player_rolling()
            assert mock_read.call_count == calls_after_first

            # With force_refresh — re-reads
            load_player_rolling(force_refresh=True)
            assert mock_read.call_count > calls_after_first

    def test_team_rolling_force_refresh_re_reads(
        self, _clean_rolling_cache: None,
    ) -> None:
        with patch(
            "scoutfootball.app.data_loader._safe_read_parquet",
        ) as mock_read:
            load_team_rolling()
            calls_after_first = mock_read.call_count

            load_team_rolling()
            assert mock_read.call_count == calls_after_first

            load_team_rolling(force_refresh=True)
            assert mock_read.call_count > calls_after_first

    def test_player_rolling_force_refresh_returns_dataframe(
        self, _clean_rolling_cache: None,
    ) -> None:
        # Populate cache
        load_player_rolling()
        assert _PLAYER_KEY in _ttl_cache._store
        df = load_player_rolling(force_refresh=True)
        assert isinstance(df, pd.DataFrame)
        # Cache was repopulated
        assert _PLAYER_KEY in _ttl_cache._store

    def test_team_rolling_force_refresh_returns_dataframe(
        self, _clean_rolling_cache: None,
    ) -> None:
        load_team_rolling()
        assert _TEAM_KEY in _ttl_cache._store
        df = load_team_rolling(force_refresh=True)
        assert isinstance(df, pd.DataFrame)
        assert _TEAM_KEY in _ttl_cache._store


# ---------------------------------------------------------------------------
# NOT using lru_cache
# ---------------------------------------------------------------------------


class TestRollingLoadersNotUsingLruCache:
    """The migrated loaders must not be decorated with functools.lru_cache."""

    def test_load_player_rolling_has_no_cache_info(self) -> None:
        # lru_cache-decorated functions expose a .cache_info() method.
        assert not hasattr(load_player_rolling, "cache_info")
        assert not hasattr(load_player_rolling, "cache_clear")

    def test_load_team_rolling_has_no_cache_info(self) -> None:
        assert not hasattr(load_team_rolling, "cache_info")
        assert not hasattr(load_team_rolling, "cache_clear")

    def test_player_cache_goes_through_ttl_cache(self) -> None:
        """The cache key is registered in _ttl_cache._store, not in an
        lru_cache internal structure."""
        _ttl_cache.invalidate(_PLAYER_KEY)
        try:
            load_player_rolling()
            # Entry must be in the TTL store, and retrievable via .get()
            cached = _ttl_cache.get(_PLAYER_KEY)
            assert cached is not _MISSING
            assert isinstance(cached, pd.DataFrame)
        finally:
            _ttl_cache.invalidate(_PLAYER_KEY)

    def test_team_cache_goes_through_ttl_cache(self) -> None:
        _ttl_cache.invalidate(_TEAM_KEY)
        try:
            load_team_rolling()
            cached = _ttl_cache.get(_TEAM_KEY)
            assert cached is not _MISSING
            assert isinstance(cached, pd.DataFrame)
        finally:
            _ttl_cache.invalidate(_TEAM_KEY)
