"""Normalization helpers for cross-source entity matching."""

from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher

import pandas as pd

TEAM_STOPWORDS = {
    "ac",
    "afc",
    "athletic",
    "atletico",
    "cf",
    "club",
    "fc",
    "fk",
    "football",
    "sc",
    "sfc",
    "sporting",
    "sv",
    "the",
}
COUNTRY_ALIASES = {
    "eng": "england",
    "en": "england",
    "gb": "united kingdom",
    "uk": "united kingdom",
    "es": "spain",
    "esp": "spain",
    "de": "germany",
    "ger": "germany",
    "fr": "france",
    "fra": "france",
    "it": "italy",
    "ita": "italy",
    "nl": "netherlands",
    "ned": "netherlands",
    "por": "portugal",
    "pt": "portugal",
    "usa": "united states",
    "us": "united states",
    "u s a": "united states",
}
POSITION_ALIASES = {
    "goalkeeper": "gk",
    "keeper": "gk",
    "gk": "gk",
    "defender": "def",
    "center back": "cb",
    "centre back": "cb",
    "full back": "fb",
    "wing back": "wb",
    "midfielder": "mid",
    "attacking midfielder": "am",
    "defensive midfielder": "dm",
    "forward": "fwd",
    "striker": "fwd",
    "winger": "wing",
    # Understat-style single letters and combos
    "d": "cb",
    "m": "cm",
    "f": "st",
    "s": "st",
    "d m": "fb",
    "d s": "cb",
    "d m s": "fb",
    "d f": "cb",
    "f m": "am",
    "f m s": "w",
    "f s": "st",
    # FBref-style abbreviations and combos
    "df": "cb",
    "mf": "cm",
    "fw": "st",
    "df mf": "fb",
    "mf fw": "am",
    "fw mf": "w",
}
NON_ALNUM_PATTERN = re.compile(r"[^a-z0-9\s]+")
MULTISPACE_PATTERN = re.compile(r"\s+")


def normalize_person_name(name: str | None) -> str:
    """Normalize a player/person name for deterministic matching."""

    return _normalize_core(name)


TEAM_NAME_ALIASES: dict[str, str] = {
    # Premier League
    "arsenal": "Arsenal",
    "aston villa": "Aston Villa",
    "bournemouth": "Bournemouth",
    "brentford": "Brentford",
    "brighton": "Brighton",
    "brighton and hove albion": "Brighton",
    "burnley": "Burnley",
    "chelsea": "Chelsea",
    "crystal palace": "Crystal Palace",
    "everton": "Everton",
    "fulham": "Fulham",
    "ipswich town": "Ipswich",
    "ipswich": "Ipswich",
    "leeds united": "Leeds",
    "leeds": "Leeds",
    "leicester city": "Leicester",
    "leicester": "Leicester",
    "liverpool": "Liverpool",
    "luton town": "Luton",
    "luton": "Luton",
    "man city": "Manchester City",
    "manchester city": "Manchester City",
    "man utd": "Manchester United",
    "man united": "Manchester United",
    "manchester utd": "Manchester United",
    "manchester united": "Manchester United",
    "newcastle united": "Newcastle",
    "newcastle": "Newcastle",
    "norwich city": "Norwich",
    "norwich": "Norwich",
    "nottingham forest": "Nott'm Forest",
    "nottm forest": "Nott'm Forest",
    "sheffield united": "Sheffield United",
    "sheffield utd": "Sheffield United",
    "southampton": "Southampton",
    "spurs": "Tottenham",
    "tottenham": "Tottenham",
    "tottenham hotspur": "Tottenham",
    "watford": "Watford",
    "west bromwich albion": "West Brom",
    "west brom": "West Brom",
    "west ham united": "West Ham",
    "west ham": "West Ham",
    "wolverhampton wanderers": "Wolves",
    "wolverhampton": "Wolves",
    "wolves": "Wolves",
    # La Liga
    "alaves": "Alaves",
    "deportivo alaves": "Alaves",
    "athletic bilbao": "Ath Bilbao",
    "athletic club": "Ath Bilbao",
    "atletico": "Ath Madrid",
    "atletico madrid": "Ath Madrid",
    "barca": "Barcelona",
    "barcelona": "Barcelona",
    "fc barcelona": "Barcelona",
    "betis": "Betis",
    "real betis": "Betis",
    "cadiz": "Cadiz",
    "cadiz cf": "Cadiz",
    "celta": "Celta",
    "celta vigo": "Celta",
    "deportivo": "La Coruna",
    "deportivo la coruna": "La Coruna",
    "eibar": "Eibar",
    "elche": "Elche",
    "espanyol": "Espanol",
    "rcd espanyol": "Espanol",
    "getafe": "Getafe",
    "girona": "Girona",
    "girona fc": "Girona",
    "granada": "Granada",
    "granada cf": "Granada",
    "huesca": "Huesca",
    "sd huesca": "Huesca",
    "leganes": "Leganes",
    "cd leganes": "Leganes",
    "levante": "Levante",
    "mallorca": "Mallorca",
    "rcd mallorca": "Mallorca",
    "osasuna": "Osasuna",
    "rayo": "Rayo Vallecano",
    "rayo vallecano": "Rayo Vallecano",
    "real madrid": "Real Madrid",
    "real sociedad": "Real Sociedad",
    "sevilla": "Sevilla",
    "sevilla fc": "Sevilla",
    "valencia": "Valencia",
    "valencia cf": "Valencia",
    "valladolid": "Valladolid",
    "real valladolid": "Valladolid",
    "villarreal": "Villarreal",
    "villarreal cf": "Villarreal",
    "las palmas": "Las Palmas",
    "ud las palmas": "Las Palmas",
    "almeria": "Almeria",
    "ud almeria": "Almeria",
    # Bundesliga
    "augsburg": "Augsburg",
    "fc augsburg": "Augsburg",
    "bayer leverkusen": "Leverkusen",
    "leverkusen": "Leverkusen",
    "bayern": "Bayern Munich",
    "bayern munich": "Bayern Munich",
    "bayern munchen": "Bayern Munich",
    "fc bayern munich": "Bayern Munich",
    "borussia dortmund": "Dortmund",
    "dortmund": "Dortmund",
    "borussia monchengladbach": "M'gladbach",
    "borussia mgladbach": "M'gladbach",
    "borussia m.gladbach": "M'gladbach",
    "monchengladbach": "M'gladbach",
    "gladbach": "M'gladbach",
    "bielefeld": "Arminia Bielefeld",
    "arminia bielefeld": "Arminia Bielefeld",
    "darmstadt": "Darmstadt",
    "darmstadt 98": "Darmstadt",
    "sv darmstadt": "Darmstadt",
    "sv darmstadt 98": "Darmstadt",
    "eintracht": "Ein Frankfurt",
    "eintracht frankfurt": "Ein Frankfurt",
    "freiburg": "Freiburg",
    "sc freiburg": "Freiburg",
    "fortuna dusseldorf": "Fortuna Duesseldorf",
    "fortuna duesseldorf": "Fortuna Duesseldorf",
    "greuther furth": "Greuther Fuerth",
    "greuther fuerth": "Greuther Fuerth",
    "hamburg": "Hamburg",
    "hamburger sv": "Hamburg",
    "hannover": "Hannover",
    "hannover 96": "Hannover",
    "hertha": "Hertha",
    "hertha berlin": "Hertha",
    "hertha bsc": "Hertha",
    "hoffenheim": "Hoffenheim",
    "tsg hoffenheim": "Hoffenheim",
    "cologne": "Koln",
    "fc koln": "Koln",
    "koln": "Koln",
    "köln": "Koln",
    "fc cologne": "Koln",
    "leipzig": "RB Leipzig",
    "rb leipzig": "RB Leipzig",
    "rasenballsport leipzig": "RB Leipzig",
    "mainz": "Mainz",
    "mainz 05": "Mainz",
    "nurnberg": "Nuernberg",
    "nuernberg": "Nuernberg",
    "nürnberg": "Nuernberg",
    "paderborn": "Paderborn",
    "sc paderborn": "Paderborn",
    "schalke": "Schalke 04",
    "schalke 04": "Schalke 04",
    "stuttgart": "Stuttgart",
    "vfb stuttgart": "Stuttgart",
    "union berlin": "Union Berlin",
    "werder bremen": "Werder Bremen",
    "vfl wolfsburg": "Wolfsburg",
    "wolfsburg": "Wolfsburg",
    "bochum": "Bochum",
    "vfl bochum": "Bochum",
    "heidenheim": "Heidenheim",
    "fc heidenheim": "Heidenheim",
    "st pauli": "St Pauli",
    "fc st pauli": "St Pauli",
    "holstein kiel": "Holstein Kiel",
    "ingolstadt": "Ingolstadt",
    "fc ingolstadt": "Ingolstadt",
    # Serie A
    "atalanta": "Atalanta",
    "bologna": "Bologna",
    "bologna fc": "Bologna",
    "cagliari": "Cagliari",
    "cagliari calcio": "Cagliari",
    "catania": "Catania",
    "ac chievo": "Chievo",
    "chievo": "Chievo",
    "empoli": "Empoli",
    "empoli fc": "Empoli",
    "acf fiorentina": "Fiorentina",
    "fiorentina": "Fiorentina",
    "frosinone": "Frosinone",
    "genoa": "Genoa",
    "genoa cfc": "Genoa",
    "hellas verona": "Verona",
    "verona": "Verona",
    "inter": "Inter",
    "inter milan": "Inter",
    "inter milano": "Inter",
    "internazionale": "Inter",
    "fc internazionale": "Inter",
    "juventus": "Juventus",
    "juve": "Juventus",
    "lazio": "Lazio",
    "ss lazio": "Lazio",
    "lecce": "Lecce",
    "us lecce": "Lecce",
    "ac milan": "Milan",
    "milan": "Milan",
    "napoli": "Napoli",
    "ssc napoli": "Napoli",
    "parma": "Parma",
    "parma calcio": "Parma",
    "pescara": "Pescara",
    "as roma": "Roma",
    "roma": "Roma",
    "salernitana": "Salernitana",
    "sassuolo": "Sassuolo",
    "spezia": "Spezia",
    "torino": "Torino",
    "torino fc": "Torino",
    "udinese": "Udinese",
    "udinese calcio": "Udinese",
    "venezia": "Venezia",
    "venezia fc": "Venezia",
    "cittadella": "Cittadella",
    "benevento": "Benevento",
    "brescia": "Brescia",
    "ac monza": "Monza",
    "monza": "Monza",
    "como": "Como",
    "como 1907": "Como",
    "cremonese": "Cremonese",
    "us cremonese": "Cremonese",
    # Ligue 1
    "lens": "Lens",
    "rc lens": "Lens",
    "lens rc": "Lens",
    "lille": "Lille",
    "lille osc": "Lille",
    "lyon": "Lyon",
    "olympique lyonnais": "Lyon",
    "marseille": "Marseille",
    "olympique marseille": "Marseille",
    "om": "Marseille",
    "monaco": "Monaco",
    "as monaco": "Monaco",
    "montpellier": "Montpellier",
    "montpellier hsc": "Montpellier",
    "nantes": "Nantes",
    "fc nantes": "Nantes",
    "nice": "Nice",
    "ogc nice": "Nice",
    "paris saint-germain": "Paris SG",
    "paris saint-germain fc": "Paris SG",
    "paris sg": "Paris SG",
    "paris saint germain": "Paris SG",
    "psg": "Paris SG",
    "reims": "Reims",
    "stade de reims": "Reims",
    "rennes": "Rennes",
    "stade rennais": "Rennes",
    "saint-etienne": "St Etienne",
    "saint etienne": "St Etienne",
    "as saint-etienne": "St Etienne",
    "strasbourg": "Strasbourg",
    "rc strasbourg": "Strasbourg",
    "toulouse": "Toulouse",
    "toulouse fc": "Toulouse",
    "bordeaux": "Bordeaux",
    "girondins bordeaux": "Bordeaux",
    "metz": "Metz",
    "fc metz": "Metz",
    "amiens": "Amiens",
    "sc amiens": "Amiens",
    "angers": "Angers",
    "angers sco": "Angers",
    "brest": "Brest",
    "stade brestois": "Brest",
    "clermont": "Clermont",
    "clermont foot": "Clermont",
    "le havre": "Le Havre",
    "fc lorient": "Lorient",
    "lorient": "Lorient",
    "ac ajaccio": "Ajaccio",
    "ajaccio": "Ajaccio",
    "troyes": "Troyes",
    "estac troyes": "Troyes",
    "dijon": "Dijon",
    "dijon fco": "Dijon",
    "caen": "Caen",
    "sm caen": "Caen",
    "nimes": "Nimes",
    "nimes olympique": "Nimes",
    "auxerre": "Auxerre",
    "aj auxerre": "Auxerre",
    # Other European
    "benfica": "SL Benfica",
    "porto": "FC Porto",
    "sporting": "Sporting CP",
    "sporting lisbon": "Sporting CP",
    "ajax": "AFC Ajax",
    "galatasaray": "Galatasaray SK",
    "fenerbahce": "Fenerbahçe SK",
    "besiktas": "Beşiktaş JK",
    "celtic": "Celtic FC",
    "rangers": "Rangers FC",
    "club brugge": "Club Brugge KV",
}


def normalize_team_name(name: str | None) -> str:
    """Normalize a team name to its canonical form.

    Strips accents, lowercases, and looks up in TEAM_NAME_ALIASES.
    Falls back to the original stripped name if no alias is found.
    Returns empty string for None / NaN / blank input.
    """
    if not name or pd.isna(name):
        return ""
    stripped = str(name).strip()
    # Strip accents for matching (e.g. Köln -> Koln)
    normalized = unicodedata.normalize("NFKD", stripped)
    ascii_name = "".join(c for c in normalized if not unicodedata.combining(c))
    lower = ascii_name.strip().lower()
    return TEAM_NAME_ALIASES.get(lower, stripped)


def normalize_country_name(country: str | None) -> str:
    """Normalize country names and short aliases."""

    normalized = _normalize_core(country)
    if not normalized:
        return ""
    return COUNTRY_ALIASES.get(normalized, normalized)


def normalize_position_group(position: str | None) -> str:
    """Normalize loose position labels into comparable groups."""

    normalized = _normalize_core(position)
    if not normalized:
        return ""
    return POSITION_ALIASES.get(normalized, normalized)


def _normalize_core(value: str | None) -> str:
    if value is None:
        return ""
    text = str(value).strip().lower()
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(character for character in text if not unicodedata.combining(character))
    text = text.replace("&", " and ")
    text = text.replace("/", " ")
    text = NON_ALNUM_PATTERN.sub(" ", text)
    text = MULTISPACE_PATTERN.sub(" ", text)
    return text.strip()


def build_player_composite_key(
    name: str,
    born_year: int | None = None,
    nationality: str | None = None,
) -> str:
    """Build a composite key for cross-source player identity matching.

    Format: "{normalized_name}|{born_year}|{normalized_nationality}"
    Missing components are replaced with "NA".
    """
    normalized_name = normalize_person_name(name)
    year_str = str(born_year) if born_year is not None else "NA"
    nat_str = normalize_country_name(nationality) if nationality is not None else "NA"
    return f"{normalized_name}|{year_str}|{nat_str}"


def fuzzy_match_player_key(
    key1: str,
    key2: str,
    *,
    name_similarity_threshold: float = 0.85,
) -> bool:
    """Check if two composite keys likely refer to the same player.

    Uses exact match on born_year and nationality, with fuzzy matching on name.
    """
    parts1 = key1.split("|")
    parts2 = key2.split("|")
    if len(parts1) != 3 or len(parts2) != 3:
        return False

    name1, year1, nat1 = parts1
    name2, year2, nat2 = parts2

    # born_year must match exactly (unless either is "NA")
    if year1 != "NA" and year2 != "NA" and year1 != year2:
        return False

    # nationality must match exactly (unless either is "NA")
    if nat1 != "NA" and nat2 != "NA" and nat1 != nat2:
        return False

    # fuzzy match on name
    similarity = SequenceMatcher(None, name1, name2).ratio()
    return similarity >= name_similarity_threshold
