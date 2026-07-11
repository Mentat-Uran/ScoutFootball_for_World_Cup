"""Static data for the 2026 FIFA World Cup (US/Canada/Mexico).

48 teams, 12 groups (A-L), June 11 - July 19 2026.
Group and squad data are built-in; match schedules are generated from the
official fixture pattern.  Squad rosters are expected call-ups based on
recent national team selections and 2025-26 club form — they will be updated
once official 26-man squads are announced.
"""

from __future__ import annotations

from dataclasses import dataclass

# ── Groups ────────────────────────────────────────────────────────────────

GROUPS: dict[str, list[str]] = {
    "A": ["Mexico", "South Africa", "South Korea", "Czech Republic"],
    "B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["United States", "Paraguay", "Australia", "Turkey"],
    "E": ["Germany", "Curacao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"],
}

# Mapping: national team name -> common club-league country for rating lookup
NATIONALITY_TO_LEAGUE_COUNTRY: dict[str, list[str]] = {
    "Mexico": ["MEX"], "South Africa": ["RSA"], "South Korea": ["KOR"],
    "Czech Republic": ["CZE"], "Canada": ["CAN"],
    "Bosnia and Herzegovina": ["BIH"], "Qatar": ["QAT"], "Switzerland": ["SUI"],
    "Brazil": ["BRA"], "Morocco": ["MAR"], "Haiti": ["HAI"], "Scotland": ["SCO"],
    "United States": ["USA"], "Paraguay": ["PAR"], "Australia": ["AUS"],
    "Turkey": ["TUR"], "Germany": ["GER"], "Curacao": ["CUW"],
    "Ivory Coast": ["CIV"], "Ecuador": ["ECU"], "Netherlands": ["NED"],
    "Japan": ["JPN"], "Sweden": ["SWE"], "Tunisia": ["TUN"],
    "Belgium": ["BEL"], "Egypt": ["EGY"], "Iran": ["IRN"],
    "New Zealand": ["NZL"], "Spain": ["ESP"], "Cape Verde": ["CPV"],
    "Saudi Arabia": ["KSA"], "Uruguay": ["URU"], "France": ["FRA"],
    "Senegal": ["SEN"], "Iraq": ["IRQ"], "Norway": ["NOR"],
    "Argentina": ["ARG"], "Algeria": ["ALG"], "Austria": ["AUT"],
    "Jordan": ["JOR"], "Portugal": ["POR"], "DR Congo": ["COD"],
    "Uzbekistan": ["UZB"], "Colombia": ["COL"], "England": ["ENG"],
    "Croatia": ["CRO"], "Ghana": ["GHA"], "Panama": ["PAN"],
}

# FIFA country codes (3-letter)
FIFA_CODES: dict[str, str] = {
    "Mexico": "MEX", "South Africa": "RSA", "South Korea": "KOR",
    "Czech Republic": "CZE", "Canada": "CAN",
    "Bosnia and Herzegovina": "BIH", "Qatar": "QAT", "Switzerland": "SUI",
    "Brazil": "BRA", "Morocco": "MAR", "Haiti": "HAI", "Scotland": "SCO",
    "United States": "USA", "Paraguay": "PAR", "Australia": "AUS",
    "Turkey": "TUR", "Germany": "GER", "Curacao": "CUW",
    "Ivory Coast": "CIV", "Ecuador": "ECU", "Netherlands": "NED",
    "Japan": "JPN", "Sweden": "SWE", "Tunisia": "TUN",
    "Belgium": "BEL", "Egypt": "EGY", "Iran": "IRN",
    "New Zealand": "NZL", "Spain": "ESP", "Cape Verde": "CPV",
    "Saudi Arabia": "KSA", "Uruguay": "URU", "France": "FRA",
    "Senegal": "SEN", "Iraq": "IRQ", "Norway": "NOR",
    "Argentina": "ARG", "Algeria": "ALG", "Austria": "AUT",
    "Jordan": "JOR", "Portugal": "POR", "DR Congo": "COD",
    "Uzbekistan": "UZB", "Colombia": "COL", "England": "ENG",
    "Croatia": "CRO", "Ghana": "GHA", "Panama": "PAN",
}

HOSTS = ["United States", "Canada", "Mexico"]
TOURNAMENT_START = "2026-06-11"
TOURNAMENT_END = "2026-07-19"

OPTA_WIN_PROBABILITY: dict[str, float] = {
    "Spain": 0.161, "France": 0.128, "Brazil": 0.112,
    "England": 0.098, "Argentina": 0.087, "Germany": 0.072,
    "Portugal": 0.065, "Netherlands": 0.054, "Uruguay": 0.038,
    "Belgium": 0.032,
}
WIN_PROBABILITY = OPTA_WIN_PROBABILITY


# ── Match schedule ────────────────────────────────────────────────────────

@dataclass
class Match:
    matchday: int
    date: str
    time_et: str
    home: str
    away: str
    venue: str
    city: str
    group: str | None = None
    stage: str = "Group Stage"


def generate_group_stage_matches() -> list[Match]:
    """Generate all 72 group-stage matches (12 groups x 6 matches each).

    Uses the official 2026 FIFA World Cup fixture schedule (all times ET).
    """
    schedule: list[tuple[str, int, str, str, str, str, str, str]] = [
        # (group, matchday, date, time_et, home, away, venue, city)
        # Group A
        ("A", 1, "2026-06-11", "15:00", "Mexico", "South Africa", "Estadio Azteca", "Mexico City"),
        ("A", 1, "2026-06-11", "22:00", "South Korea", "Czech Republic", "Estadio Akron", "Guadalajara"),
        ("A", 2, "2026-06-18", "12:00", "South Africa", "Czech Republic", "Mercedes-Benz Stadium", "Atlanta"),
        ("A", 2, "2026-06-18", "21:00", "Mexico", "South Korea", "Estadio Akron", "Guadalajara"),
        ("A", 3, "2026-06-24", "21:00", "Mexico", "Czech Republic", "Estadio Azteca", "Mexico City"),
        ("A", 3, "2026-06-24", "21:00", "South Africa", "South Korea", "Estadio BBVA", "Monterrey"),
        # Group B
        ("B", 1, "2026-06-12", "15:00", "Canada", "Bosnia and Herzegovina", "BMO Field", "Toronto"),
        ("B", 1, "2026-06-13", "15:00", "Qatar", "Switzerland", "Levi's Stadium", "San Francisco Bay Area"),
        ("B", 2, "2026-06-18", "15:00", "Bosnia and Herzegovina", "Switzerland", "SoFi Stadium", "Los Angeles"),
        ("B", 2, "2026-06-18", "18:00", "Canada", "Qatar", "BC Place", "Vancouver"),
        ("B", 3, "2026-06-24", "15:00", "Bosnia and Herzegovina", "Qatar", "Lumen Field", "Seattle"),
        ("B", 3, "2026-06-24", "15:00", "Canada", "Switzerland", "BC Place", "Vancouver"),
        # Group C
        ("C", 1, "2026-06-13", "18:00", "Brazil", "Morocco", "MetLife Stadium", "New York/New Jersey"),
        ("C", 1, "2026-06-13", "21:00", "Haiti", "Scotland", "Gillette Stadium", "Boston"),
        ("C", 2, "2026-06-19", "18:00", "Morocco", "Scotland", "Gillette Stadium", "Boston"),
        ("C", 2, "2026-06-19", "21:00", "Haiti", "Brazil", "Lincoln Financial Field", "Philadelphia"),
        ("C", 3, "2026-06-24", "18:00", "Morocco", "Haiti", "Mercedes-Benz Stadium", "Atlanta"),
        ("C", 3, "2026-06-24", "18:00", "Brazil", "Scotland", "Hard Rock Stadium", "Miami"),
        # Group D
        ("D", 1, "2026-06-12", "21:00", "United States", "Paraguay", "SoFi Stadium", "Los Angeles"),
        ("D", 1, "2026-06-13", "00:00", "Australia", "Turkey", "BC Place", "Vancouver"),
        ("D", 2, "2026-06-19", "00:00", "Paraguay", "Turkey", "Levi's Stadium", "San Francisco Bay Area"),
        ("D", 2, "2026-06-19", "15:00", "United States", "Australia", "Lumen Field", "Seattle"),
        ("D", 3, "2026-06-25", "22:00", "United States", "Turkey", "SoFi Stadium", "Los Angeles"),
        ("D", 3, "2026-06-25", "22:00", "Paraguay", "Australia", "Levi's Stadium", "San Francisco Bay Area"),
        # Group E
        ("E", 1, "2026-06-14", "13:00", "Germany", "Curacao", "NRG Stadium", "Houston"),
        ("E", 1, "2026-06-14", "19:00", "Ivory Coast", "Ecuador", "Lincoln Financial Field", "Philadelphia"),
        ("E", 2, "2026-06-20", "16:00", "Germany", "Ivory Coast", "BMO Field", "Toronto"),
        ("E", 2, "2026-06-20", "20:00", "Curacao", "Ecuador", "Arrowhead Stadium", "Kansas City"),
        ("E", 3, "2026-06-25", "16:00", "Germany", "Ecuador", "MetLife Stadium", "New York/New Jersey"),
        ("E", 3, "2026-06-25", "16:00", "Curacao", "Ivory Coast", "Lincoln Financial Field", "Philadelphia"),
        # Group F
        ("F", 1, "2026-06-14", "16:00", "Netherlands", "Japan", "AT&T Stadium", "Dallas"),
        ("F", 1, "2026-06-14", "19:00", "Sweden", "Tunisia", "Estadio BBVA", "Monterrey"),
        ("F", 2, "2026-06-20", "13:00", "Netherlands", "Sweden", "NRG Stadium", "Houston"),
        ("F", 2, "2026-06-20", "00:00", "Japan", "Tunisia", "Estadio BBVA", "Monterrey"),
        ("F", 3, "2026-06-25", "19:00", "Netherlands", "Tunisia", "Arrowhead Stadium", "Kansas City"),
        ("F", 3, "2026-06-25", "19:00", "Japan", "Sweden", "AT&T Stadium", "Dallas"),
        # Group G
        ("G", 1, "2026-06-15", "15:00", "Belgium", "Egypt", "Lumen Field", "Seattle"),
        ("G", 1, "2026-06-15", "21:00", "Iran", "New Zealand", "SoFi Stadium", "Los Angeles"),
        ("G", 2, "2026-06-21", "15:00", "Belgium", "Iran", "SoFi Stadium", "Los Angeles"),
        ("G", 2, "2026-06-21", "21:00", "Egypt", "New Zealand", "BC Place", "Vancouver"),
        ("G", 3, "2026-06-26", "23:00", "Belgium", "New Zealand", "BC Place", "Vancouver"),
        ("G", 3, "2026-06-26", "23:00", "Egypt", "Iran", "Lumen Field", "Seattle"),
        # Group H
        ("H", 1, "2026-06-15", "12:00", "Spain", "Cape Verde", "Mercedes-Benz Stadium", "Atlanta"),
        ("H", 1, "2026-06-15", "18:00", "Saudi Arabia", "Uruguay", "Hard Rock Stadium", "Miami"),
        ("H", 2, "2026-06-21", "12:00", "Spain", "Saudi Arabia", "Mercedes-Benz Stadium", "Atlanta"),
        ("H", 2, "2026-06-21", "18:00", "Cape Verde", "Uruguay", "Hard Rock Stadium", "Miami"),
        ("H", 3, "2026-06-26", "20:00", "Spain", "Uruguay", "Estadio Akron", "Guadalajara"),
        ("H", 3, "2026-06-26", "20:00", "Cape Verde", "Saudi Arabia", "NRG Stadium", "Houston"),
        # Group I
        ("I", 1, "2026-06-16", "15:00", "France", "Senegal", "MetLife Stadium", "New York/New Jersey"),
        ("I", 1, "2026-06-16", "18:00", "Iraq", "Norway", "Gillette Stadium", "Boston"),
        ("I", 2, "2026-06-22", "17:00", "France", "Iraq", "Lincoln Financial Field", "Philadelphia"),
        ("I", 2, "2026-06-22", "20:00", "Senegal", "Norway", "MetLife Stadium", "New York/New Jersey"),
        ("I", 3, "2026-06-26", "15:00", "France", "Norway", "Gillette Stadium", "Boston"),
        ("I", 3, "2026-06-26", "15:00", "Iraq", "Senegal", "BMO Field", "Toronto"),
        # Group J
        ("J", 1, "2026-06-16", "21:00", "Argentina", "Algeria", "Arrowhead Stadium", "Kansas City"),
        ("J", 1, "2026-06-16", "00:00", "Austria", "Jordan", "Levi's Stadium", "San Francisco Bay Area"),
        ("J", 2, "2026-06-22", "13:00", "Argentina", "Austria", "AT&T Stadium", "Dallas"),
        ("J", 2, "2026-06-22", "23:00", "Algeria", "Jordan", "Levi's Stadium", "San Francisco Bay Area"),
        ("J", 3, "2026-06-27", "22:00", "Argentina", "Jordan", "AT&T Stadium", "Dallas"),
        ("J", 3, "2026-06-27", "22:00", "Algeria", "Austria", "Arrowhead Stadium", "Kansas City"),
        # Group K
        ("K", 1, "2026-06-17", "13:00", "Portugal", "DR Congo", "NRG Stadium", "Houston"),
        ("K", 1, "2026-06-17", "22:00", "Uzbekistan", "Colombia", "Estadio Azteca", "Mexico City"),
        ("K", 2, "2026-06-23", "13:00", "Portugal", "Uzbekistan", "NRG Stadium", "Houston"),
        ("K", 2, "2026-06-23", "22:00", "DR Congo", "Colombia", "Estadio Akron", "Guadalajara"),
        ("K", 3, "2026-06-27", "19:30", "Portugal", "Colombia", "Hard Rock Stadium", "Miami"),
        ("K", 3, "2026-06-27", "19:30", "DR Congo", "Uzbekistan", "Mercedes-Benz Stadium", "Atlanta"),
        # Group L
        ("L", 1, "2026-06-17", "16:00", "England", "Croatia", "AT&T Stadium", "Dallas"),
        ("L", 1, "2026-06-17", "19:00", "Ghana", "Panama", "BMO Field", "Toronto"),
        ("L", 2, "2026-06-23", "16:00", "England", "Ghana", "Gillette Stadium", "Boston"),
        ("L", 2, "2026-06-23", "19:00", "Croatia", "Panama", "BMO Field", "Toronto"),
        ("L", 3, "2026-06-27", "17:00", "England", "Panama", "MetLife Stadium", "New York/New Jersey"),
        ("L", 3, "2026-06-27", "17:00", "Croatia", "Ghana", "Lincoln Financial Field", "Philadelphia"),
    ]

    return [
        Match(
            matchday=md, date=date, time_et=time_et,
            home=home, away=away, venue=venue, city=city,
            group=group, stage="Group Stage",
        )
        for group, md, date, time_et, home, away, venue, city in schedule
    ]


# ── Squad data ────────────────────────────────────────────────────────────

@dataclass
class SquadPlayer:
    name: str
    position: str  # GK/CB/FB/DM/CM/AM/W/ST
    club: str
    club_league: str
    has_rating: bool = False
    rating: float | None = None
    rating_confidence: str = "none"


SQUADS: dict[str, list[dict]] = {
    "Algeria": [
        {"name": "Riyad Mahrez", "position": "W", "club": "Al-Ahli", "club_league": "SPL"},
        {"name": "Rayan Ait-Nouri", "position": "FB", "club": "Wolves", "club_league": "Premier League"},
        {"name": "Ismael Bennacer", "position": "CM", "club": "AC Milan", "club_league": "Serie A"},
        {"name": "Ramy Bensebaini", "position": "CB", "club": "Dortmund", "club_league": "Bundesliga"},
        {"name": "Houssem Aouar", "position": "AM", "club": "Al-Ittihad", "club_league": "SPL"},
        {"name": "Amine Gouiri", "position": "ST", "club": "Marseille", "club_league": "Ligue 1"},
        {"name": "Islam Slimani", "position": "ST", "club": "Mechelen", "club_league": "Jupiler Pro League"},
        {"name": "Hichem Boudaoui", "position": "CM", "club": "Nice", "club_league": "Ligue 1"},
        {"name": "Adam Ounas", "position": "W", "club": "Lille", "club_league": "Ligue 1"},
        {"name": "Said Benrahma", "position": "W", "club": "Lyon", "club_league": "Ligue 1"},
        {"name": "Fares Chaibi", "position": "W", "club": "Ein Frankfurt", "club_league": "Bundesliga"},
        {"name": "Nabil Bentaleb", "position": "CM", "club": "Lille", "club_league": "Ligue 1"},
        {"name": "Yacine Adli", "position": "AM", "club": "Fiorentina", "club_league": "Serie A"},
        {"name": "Alexandre Oukidja", "position": "GK", "club": "Metz", "club_league": "Ligue 1"},
        {"name": "Andy Delort", "position": "ST", "club": "Montpellier", "club_league": "Ligue 1"},
        {"name": "Nabil Fekir", "position": "AM", "club": "Betis", "club_league": "La Liga"},
        {"name": "Maghnes Akliouche", "position": "W", "club": "Monaco", "club_league": "Ligue 1"},
        {"name": "Ryad Boudebouz", "position": "W", "club": "Montpellier", "club_league": "Ligue 1"},
        {"name": "Maxime Lopez", "position": "CM", "club": "Sassuolo", "club_league": "Serie A"},
        {"name": "Ishak Belfodil", "position": "ST", "club": "Brest", "club_league": "Ligue 1"},
        {"name": "Ibrahim Maza", "position": "AM", "club": "Leverkusen", "club_league": "Bundesliga"},
        {"name": "Farid Boulaya", "position": "W", "club": "Metz", "club_league": "Ligue 1"},
        {"name": "Djamel Benlamri", "position": "CB", "club": "Qatar SC", "club_league": "Qatar Stars League"},
        {"name": "Aissa Mandi", "position": "CB", "club": "Villarreal", "club_league": "La Liga"},
        {"name": "Moustapha Zeghba", "position": "GK", "club": "Almeria", "club_league": "La Liga"},
        {"name": "Mehdi Zeffane", "position": "FB", "club": "Clermont", "club_league": "Ligue 1"},
    ],
    "Argentina": [
        {"name": "Emiliano Martinez", "position": "GK", "club": "Aston Villa", "club_league": "Premier League"},
        {"name": "Juan Musso", "position": "GK", "club": "Atletico Madrid", "club_league": "La Liga"},
        {"name": "Geronimo Rulli", "position": "GK", "club": "Marseille", "club_league": "Ligue 1"},
        {"name": "Cristian Romero", "position": "CB", "club": "Tottenham", "club_league": "Premier League"},
        {"name": "Lisandro Martinez", "position": "CB", "club": "Manchester United", "club_league": "Premier League"},
        {"name": "Nicolas Otamendi", "position": "CB", "club": "Benfica", "club_league": "Liga Portugal"},
        {"name": "Leonardo Balerdi", "position": "CB", "club": "Marseille", "club_league": "Ligue 1"},
        {"name": "Facundo Medina", "position": "CB", "club": "Marseille", "club_league": "Ligue 1"},
        {"name": "Nicolas Tagliafico", "position": "FB", "club": "Lyon", "club_league": "Ligue 1"},
        {"name": "Gonzalo Montiel", "position": "FB", "club": "River Plate", "club_league": "Liga Profesional"},
        {"name": "Nahuel Molina", "position": "FB", "club": "Atletico Madrid", "club_league": "La Liga"},
        {"name": "Valentin Barco", "position": "FB", "club": "Strasbourg", "club_league": "Ligue 1"},
        {"name": "Leandro Paredes", "position": "DM", "club": "Boca Juniors", "club_league": "Liga Profesional"},
        {"name": "Rodrigo De Paul", "position": "CM", "club": "Inter Miami", "club_league": "MLS"},
        {"name": "Alexis Mac Allister", "position": "CM", "club": "Liverpool", "club_league": "Premier League"},
        {"name": "Enzo Fernandez", "position": "CM", "club": "Chelsea", "club_league": "Premier League"},
        {"name": "Exequiel Palacios", "position": "CM", "club": "Bayer Leverkusen", "club_league": "Bundesliga"},
        {"name": "Lionel Messi", "position": "AM", "club": "Inter Miami", "club_league": "MLS"},
        {"name": "Giovani Lo Celso", "position": "AM", "club": "Real Betis", "club_league": "La Liga"},
        {"name": "Thiago Almada", "position": "AM", "club": "Atletico Madrid", "club_league": "La Liga"},
        {"name": "Nico Paz", "position": "AM", "club": "Como", "club_league": "Serie A"},
        {"name": "Nicolas Gonzalez", "position": "W", "club": "Atletico Madrid", "club_league": "La Liga"},
        {"name": "Giuliano Simeone", "position": "W", "club": "Atletico Madrid", "club_league": "La Liga"},
        {"name": "Julian Alvarez", "position": "ST", "club": "Atletico Madrid", "club_league": "La Liga"},
        {"name": "Lautaro Martinez", "position": "ST", "club": "Inter Milan", "club_league": "Serie A"},
        {"name": "Jose Manuel Lopez", "position": "ST", "club": "Palmeiras", "club_league": "Brasileirao"},
    ],
    "Australia": [
        {"name": "Mathew Ryan", "position": "GK", "club": "Lens", "club_league": "Ligue 1"},
        {"name": "Harry Souttar", "position": "CB", "club": "Leicester", "club_league": "Premier League"},
        {"name": "Jackson Irvine", "position": "CM", "club": "St Pauli", "club_league": "Bundesliga"},
        {"name": "Ajdin Hrustic", "position": "AM", "club": "Salernitana", "club_league": "Serie A"},
        {"name": "Alessandro Circati", "position": "CB", "club": "Parma", "club_league": "Serie A"},
        {"name": "Cameron Burgess", "position": "CB", "club": "Ipswich", "club_league": "Premier League"},
        {"name": "Connor Metcalfe", "position": "CM", "club": "St Pauli", "club_league": "Bundesliga"},
        {"name": "Craig Goodwin", "position": "W", "club": "Al-Wehda", "club_league": "SPL"},
        {"name": "Mitchell Duke", "position": "ST", "club": "Al-Taawoun", "club_league": "SPL"},
        {"name": "Lewis Miller", "position": "FB", "club": "Hibernian", "club_league": "Scottish Premiership"},
        {"name": "Kye Rowles", "position": "CB", "club": "Hearts", "club_league": "Scottish Premiership"},
        {"name": "Riley McGree", "position": "AM", "club": "Middlesbrough", "club_league": "EFL Championship"},
        {"name": "Martin Boyle", "position": "W", "club": "Hibernian", "club_league": "Scottish Premiership"},
        {"name": "Brandon Borrello", "position": "W", "club": "Freiburg", "club_league": "Bundesliga"},
        {"name": "Denis Genreau", "position": "CM", "club": "Toulouse", "club_league": "Ligue 1"},
        {"name": "Awer Mabil", "position": "W", "club": "Kasimpasa", "club_league": "Super Lig"},
        {"name": "Joe Gauci", "position": "GK", "club": "Aston Villa", "club_league": "Premier League"},
        {"name": "Nathaniel Atkinson", "position": "FB", "club": "Hearts", "club_league": "Scottish Premiership"},
        {"name": "Kusini Yengi", "position": "ST", "club": "Portsmouth", "club_league": "EFL Championship"},
        {"name": "Cristian Volpato", "position": "W", "club": "Sassuolo", "club_league": "Serie A"},
        {"name": "Samuel Silvera", "position": "W", "club": "Middlesbrough", "club_league": "EFL Championship"},
        {"name": "Jamie Maclaren", "position": "ST", "club": "Melbourne City", "club_league": "A-League"},
        {"name": "Thomas Deng", "position": "CB", "club": "Yokohama FC", "club_league": "J-League"},
        {"name": "Danny Vukovic", "position": "GK", "club": "Central Coast Mariners", "club_league": "A-League"},
        {"name": "Trent Sainsbury", "position": "CB", "club": "Al-Wakrah", "club_league": "Qatar Stars League"},
        {"name": "Chris Ikonomidis", "position": "W", "club": "Melbourne Victory", "club_league": "A-League"},
    ],
    "Austria": [
        {"name": "David Alaba", "position": "CB", "club": "Real Madrid", "club_league": "La Liga"},
        {"name": "Marcel Sabitzer", "position": "CM", "club": "Borussia Dortmund", "club_league": "Bundesliga"},
        {"name": "Konrad Laimer", "position": "FB", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Christoph Baumgartner", "position": "AM", "club": "RB Leipzig", "club_league": "Bundesliga"},
        {"name": "Sasa Kalajdzic", "position": "ST", "club": "Wolves", "club_league": "Premier League"},
        {"name": "Kevin Danso", "position": "CB", "club": "Lens", "club_league": "Ligue 1"},
        {"name": "Patrick Wimmer", "position": "W", "club": "Wolfsburg", "club_league": "Bundesliga"},
        {"name": "Florian Kainz", "position": "W", "club": "Koln", "club_league": "Bundesliga"},
        {"name": "Marko Arnautovic", "position": "ST", "club": "Inter Milan", "club_league": "Serie A"},
        {"name": "Michael Gregoritsch", "position": "ST", "club": "Freiburg", "club_league": "Bundesliga"},
        {"name": "Valentino Lazaro", "position": "FB", "club": "Torino", "club_league": "Serie A"},
        {"name": "Marco Friedl", "position": "CB", "club": "Werder Bremen", "club_league": "Bundesliga"},
        {"name": "Philipp Lienhart", "position": "CB", "club": "Freiburg", "club_league": "Bundesliga"},
        {"name": "Stefan Lainer", "position": "FB", "club": "M'gladbach", "club_league": "Bundesliga"},
        {"name": "Alexander Prass", "position": "FB", "club": "Hoffenheim", "club_league": "Bundesliga"},
        {"name": "Sandi Lovric", "position": "CM", "club": "Udinese", "club_league": "Serie A"},
        {"name": "Kevin Stoger", "position": "CM", "club": "Bochum", "club_league": "Bundesliga"},
        {"name": "Maximilian Arnold", "position": "CM", "club": "Wolfsburg", "club_league": "Bundesliga"},
        {"name": "Karim Onisiwo", "position": "W", "club": "Mainz", "club_league": "Bundesliga"},
        {"name": "Heinz Lindner", "position": "GK", "club": "Basel", "club_league": "Swiss Super League"},
        {"name": "Pentz", "position": "GK", "club": "Braga", "club_league": "Liga Portugal"},
        {"name": "Gernot Trauner", "position": "CB", "club": "Feyenoord", "club_league": "Eredivisie"},
        {"name": "Stefan Posch", "position": "CB", "club": "Hoffenheim", "club_league": "Bundesliga"},
        {"name": "Niklas Hedl", "position": "GK", "club": "Rapid Wien", "club_league": "Austrian Bundesliga"},
        {"name": "Maximilian Wober", "position": "CB", "club": "Leeds", "club_league": "EFL Championship"},
        {"name": "Alessandro Schopf", "position": "W", "club": "Bochum", "club_league": "Bundesliga"},
    ],
    "Belgium": [
        {"name": "Kevin De Bruyne", "position": "AM", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Romelu Lukaku", "position": "ST", "club": "Napoli", "club_league": "Serie A"},
        {"name": "Thibaut Courtois", "position": "GK", "club": "Real Madrid", "club_league": "La Liga"},
        {"name": "Youri Tielemans", "position": "CM", "club": "Aston Villa", "club_league": "Premier League"},
        {"name": "Leandro Trossard", "position": "W", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Lois Openda", "position": "ST", "club": "RB Leipzig", "club_league": "Bundesliga"},
        {"name": "Charles De Ketelaere", "position": "AM", "club": "Atalanta", "club_league": "Serie A"},
        {"name": "Matz Sels", "position": "GK", "club": "Nott'm Forest", "club_league": "Premier League"},
        {"name": "Bilal El Khannouss", "position": "AM", "club": "Leicester", "club_league": "Premier League"},
        {"name": "Arthur Theate", "position": "CB", "club": "Rennes", "club_league": "Ligue 1"},
        {"name": "Wout Faes", "position": "CB", "club": "Leicester", "club_league": "Premier League"},
        {"name": "Jan Vertonghen", "position": "CB", "club": "Anderlecht", "club_league": "Jupiler Pro League"},
        {"name": "Thomas Meunier", "position": "FB", "club": "Lille", "club_league": "Ligue 1"},
        {"name": "Timothy Castagne", "position": "FB", "club": "Fulham", "club_league": "Premier League"},
        {"name": "Orel Mangala", "position": "CM", "club": "Lyon", "club_league": "Ligue 1"},
        {"name": "Amadou Onana", "position": "DM", "club": "Aston Villa", "club_league": "Premier League"},
        {"name": "Maxim De Cuyper", "position": "FB", "club": "Brighton", "club_league": "Premier League"},
        {"name": "Dodi Lukebakio", "position": "W", "club": "Sevilla", "club_league": "La Liga"},
        {"name": "Johan Bakayoko", "position": "W", "club": "PSV", "club_league": "Eredivisie"},
        {"name": "Jeremy Doku", "position": "W", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Zeno Debast", "position": "CB", "club": "Sporting CP", "club_league": "Liga Portugal"},
        {"name": "Aster Vranckx", "position": "CM", "club": "Wolfsburg", "club_league": "Bundesliga"},
        {"name": "Koen Casteels", "position": "GK", "club": "Al-Qadsiah", "club_league": "SPL"},
        {"name": "Thomas Kaminski", "position": "GK", "club": "Luton", "club_league": "EFL Championship"},
        {"name": "Mike Tresor", "position": "AM", "club": "Burnley", "club_league": "EFL Championship"},
        {"name": "Zinho Vanheusden", "position": "CB", "club": "Standard Liege", "club_league": "Jupiler Pro League"},
    ],
    "Bosnia and Herzegovina": [
        {"name": "Edin Dzeko", "position": "ST", "club": "Fenerbahce", "club_league": "Super Lig"},
        {"name": "Miralem Pjanic", "position": "CM", "club": "Sharjah", "club_league": "UAE Pro League"},
        {"name": "Sead Kolasinac", "position": "FB", "club": "Atalanta", "club_league": "Serie A"},
        {"name": "Anel Ahmedhodzic", "position": "CB", "club": "Sheffield United", "club_league": "EFL Championship"},
        {"name": "Rade Krunic", "position": "CM", "club": "Fenerbahce", "club_league": "Super Lig"},
        {"name": "Amar Dedic", "position": "FB", "club": "Marseille", "club_league": "Ligue 1"},
        {"name": "Nikola Vlasic", "position": "AM", "club": "Torino", "club_league": "Serie A"},
        {"name": "Benjamin Tahirovic", "position": "CM", "club": "Ajax", "club_league": "Eredivisie"},
        {"name": "Ermedin Demirovic", "position": "ST", "club": "Stuttgart", "club_league": "Bundesliga"},
        {"name": "Haris Tabakovic", "position": "ST", "club": "Hoffenheim", "club_league": "Bundesliga"},
        {"name": "Armin Gigovic", "position": "CM", "club": "Rosenborg", "club_league": "Eliteserien"},
        {"name": "Smail Prevljak", "position": "ST", "club": "Basaksehir", "club_league": "Super Lig"},
        {"name": "Jasmin Scuk", "position": "CM", "club": "Basaksehir", "club_league": "Super Lig"},
        {"name": "Nihad Mujakic", "position": "CB", "club": "Kasimpasa", "club_league": "Super Lig"},
        {"name": "Adrian Leon Barisic", "position": "CB", "club": "LASK", "club_league": "Austrian Bundesliga"},
        {"name": "Toni Fruk", "position": "W", "club": "Dinamo Zagreb", "club_league": "HNL"},
        {"name": "Kenan Kodro", "position": "ST", "club": "Ferencvaros", "club_league": "NB I"},
        {"name": "Nikola Vasilj", "position": "GK", "club": "St. Pauli", "club_league": "Bundesliga"},
        {"name": "Ibrahim Sehic", "position": "GK", "club": "Kasimpasa", "club_league": "Super Lig"},
        {"name": "Asim Lepinja", "position": "GK", "club": "Sarajevo", "club_league": "Premier League BiH"},
        {"name": "Dennis Hadzikadic", "position": "CM", "club": "Alanyaspor", "club_league": "Super Lig"},
        {"name": "Stevan Lukic", "position": "CB", "club": "Tuzla City", "club_league": "Premier League BiH"},
        {"name": "Cristian Martinez", "position": "FB", "club": "Zrinjski", "club_league": "Premier League BiH"},
        {"name": "Gojko Cimirot", "position": "DM", "club": "Al-Fayha", "club_league": "SPL"},
        {"name": "Sanin Prcic", "position": "CM", "club": "Monza", "club_league": "Serie A"},
        {"name": "Jozo Stanic", "position": "CB", "club": "Sturm Graz", "club_league": "Austrian Bundesliga"},
    ],
    "Brazil": [
        {"name": "Alisson", "position": "GK", "club": "Liverpool", "club_league": "Premier League"},
        {"name": "Ederson", "position": "GK", "club": "Fenerbahce", "club_league": "Super Lig"},
        {"name": "Weverton", "position": "GK", "club": "Gremio", "club_league": "Brasileirao"},
        {"name": "Marquinhos", "position": "CB", "club": "Paris Saint-Germain", "club_league": "Ligue 1"},
        {"name": "Gabriel", "position": "CB", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Bremer", "position": "CB", "club": "Juventus", "club_league": "Serie A"},
        {"name": "Roger Ibanez", "position": "CB", "club": "Al Ahli", "club_league": "SPL"},
        {"name": "Leo Pereira", "position": "CB", "club": "Flamengo", "club_league": "Brasileirao"},
        {"name": "Danilo", "position": "FB", "club": "Flamengo", "club_league": "Brasileirao"},
        {"name": "Alex Sandro", "position": "FB", "club": "Flamengo", "club_league": "Brasileirao"},
        {"name": "Douglas Santos", "position": "FB", "club": "Zenit", "club_league": "RFPL"},
        {"name": "Wesley", "position": "FB", "club": "Roma", "club_league": "Serie A"},
        {"name": "Casemiro", "position": "DM", "club": "Manchester United", "club_league": "Premier League"},
        {"name": "Fabinho", "position": "DM", "club": "Al Ittihad", "club_league": "SPL"},
        {"name": "Bruno Guimaraes", "position": "CM", "club": "Newcastle United", "club_league": "Premier League"},
        {"name": "Danilo Santos", "position": "CM", "club": "Botafogo", "club_league": "Brasileirao"},
        {"name": "Paqueta", "position": "AM", "club": "Flamengo", "club_league": "Brasileirao"},
        {"name": "Neymar", "position": "W", "club": "Al Hilal", "club_league": "SPL"},
        {"name": "Vinicius Junior", "position": "W", "club": "Real Madrid", "club_league": "La Liga"},
        {"name": "Raphinha", "position": "W", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Martinelli", "position": "W", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Luis Henrique", "position": "W", "club": "Zenit", "club_league": "RFPL"},
        {"name": "Rayyan", "position": "W", "club": "Bournemouth", "club_league": "Premier League"},
        {"name": "Endrick", "position": "ST", "club": "Lyon", "club_league": "Ligue 1"},
        {"name": "Matheus Cunha", "position": "ST", "club": "Manchester United", "club_league": "Premier League"},
        {"name": "Igor Thiago", "position": "ST", "club": "Brentford", "club_league": "Premier League"},
    ],
    "Canada": [
        {"name": "Alphonso Davies", "position": "FB", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Jonathan David", "position": "ST", "club": "Lille", "club_league": "Ligue 1"},
        {"name": "Cyle Larin", "position": "ST", "club": "Valladolid", "club_league": "La Liga"},
        {"name": "Tajon Buchanan", "position": "W", "club": "Villarreal", "club_league": "La Liga"},
        {"name": "Stephen Eustaquio", "position": "CM", "club": "Porto", "club_league": "Liga Portugal"},
        {"name": "Ismael Kone", "position": "CM", "club": "Marseille", "club_league": "Ligue 1"},
        {"name": "Derek Cornelius", "position": "CB", "club": "Marseille", "club_league": "Ligue 1"},
        {"name": "Alistair Johnston", "position": "FB", "club": "Celtic", "club_league": "Scottish Premiership"},
        {"name": "Moise Bombito", "position": "CB", "club": "Nice", "club_league": "Ligue 1"},
        {"name": "Dayne St. Clair", "position": "GK", "club": "Minnesota United", "club_league": "MLS"},
        {"name": "Maxime Crepeau", "position": "GK", "club": "Portland Timbers", "club_league": "MLS"},
        {"name": "Richie Laryea", "position": "FB", "club": "Toronto FC", "club_league": "MLS"},
        {"name": "Sam Adekugbe", "position": "FB", "club": "Vancouver Whitecaps", "club_league": "MLS"},
        {"name": "Liam Millar", "position": "W", "club": "Preston", "club_league": "EFL Championship"},
        {"name": "Junior Hoilett", "position": "W", "club": "Vancouver Whitecaps", "club_league": "MLS"},
        {"name": "Theo Corbeanu", "position": "W", "club": "Granada", "club_league": "La Liga"},
        {"name": "Jacen Russell-Rowe", "position": "ST", "club": "Columbus Crew", "club_league": "MLS"},
        {"name": "Tani Oluwaseyi", "position": "ST", "club": "Minnesota United", "club_league": "MLS"},
        {"name": "Ike Ugbo", "position": "ST", "club": "Sheffield Wednesday", "club_league": "EFL Championship"},
        {"name": "Mathieu Choiniere", "position": "CM", "club": "CF Montreal", "club_league": "MLS"},
        {"name": "Zachary Brault-Guillard", "position": "FB", "club": "CF Montreal", "club_league": "MLS"},
        {"name": "Kamal Miller", "position": "CB", "club": "Portland Timbers", "club_league": "MLS"},
        {"name": "Jonathan Osorio", "position": "CM", "club": "Toronto FC", "club_league": "MLS"},
        {"name": "Milan Borjan", "position": "GK", "club": "Al-Riyadh", "club_league": "SPL"},
        {"name": "Samuel Piette", "position": "DM", "club": "CF Montreal", "club_league": "MLS"},
        {"name": "Joel Waterman", "position": "CB", "club": "CF Montreal", "club_league": "MLS"},
    ],
    "Cape Verde": [
        {"name": "Nuno Tavares", "position": "FB", "club": "Lazio", "club_league": "Serie A"},
        {"name": "Logan Costa", "position": "CB", "club": "Toulouse", "club_league": "Ligue 1"},
        {"name": "Steven Moreira", "position": "FB", "club": "Columbus Crew", "club_league": "MLS"},
        {"name": "Diney Borges", "position": "CB", "club": "Kasimpasa", "club_league": "Super Lig"},
        {"name": "Roberto Lopes", "position": "CB", "club": "Shamrock Rovers", "club_league": "League of Ireland"},
        {"name": "Garry Rodrigues", "position": "W", "club": "Anorthosis", "club_league": "Cypriot First Division"},
        {"name": "Ryan Mendes", "position": "W", "club": "Fatih Karagumruk", "club_league": "Super Lig"},
        {"name": "Jamiro Monteiro", "position": "CM", "club": "Al-Taawoun", "club_league": "SPL"},
        {"name": "Gelson Martins", "position": "W", "club": "Olympiacos", "club_league": "Super League"},
        {"name": "Thierry Correia", "position": "FB", "club": "Valencia", "club_league": "La Liga"},
        {"name": "Kevin Pina", "position": "CM", "club": "Krasnodar", "club_league": "RFPL"},
        {"name": "Vozinha", "position": "GK", "club": "AEL Limassol", "club_league": "Cypriot First Division"},
        {"name": "Marco Soares", "position": "CM", "club": "Omonia", "club_league": "Cypriot First Division"},
        {"name": "Kiki", "position": "CB", "club": "Famalicao", "club_league": "Liga Portugal"},
        {"name": "Willyan Rocha", "position": "CB", "club": "CSKA Moscow", "club_league": "RFPL"},
        {"name": "Djaniny", "position": "ST", "club": "Al-Jazira", "club_league": "UAE Pro League"},
        {"name": "Ze Luis", "position": "ST", "club": "Spartak Moscow", "club_league": "RFPL"},
        {"name": "Patrick Andrade", "position": "CM", "club": "Qarabag", "club_league": "Azerbaijan Premier League"},
        {"name": "Deroy Duarte", "position": "CM", "club": "Spartak Moscow", "club_league": "RFPL"},
        {"name": "Ricardo Duarte", "position": "CB", "club": "Arouca", "club_league": "Liga Portugal"},
        {"name": "Joao Correia", "position": "FB", "club": "Trofense", "club_league": "Liga Portugal"},
        {"name": "Ivan Rodrigues", "position": "GK", "club": "Gil Vicente", "club_league": "Liga Portugal"},
        {"name": "Lisandro Semedo", "position": "W", "club": "Bulgarian team", "club_league": "First Professional League"},
        {"name": "Marcio Rosa", "position": "CB", "club": "Arouca", "club_league": "Liga Portugal"},
        {"name": "Kenny Rocha", "position": "CM", "club": "Nancy", "club_league": "Ligue 2"},
        {"name": "Julio Tavares", "position": "ST", "club": "Dijon", "club_league": "Ligue 2"},
    ],
    "Colombia": [
        {"name": "Luis Diaz", "position": "W", "club": "Liverpool", "club_league": "Premier League"},
        {"name": "James Rodriguez", "position": "AM", "club": "Rayo Vallecano", "club_league": "La Liga"},
        {"name": "Daniel Munoz", "position": "FB", "club": "Crystal Palace", "club_league": "Premier League"},
        {"name": "Davinson Sanchez", "position": "CB", "club": "Tottenham", "club_league": "Premier League"},
        {"name": "Yerry Mina", "position": "CB", "club": "Cagliari", "club_league": "Serie A"},
        {"name": "Jefferson Lerma", "position": "CM", "club": "Crystal Palace", "club_league": "Premier League"},
        {"name": "Jhon Cordoba", "position": "ST", "club": "Krasnodar", "club_league": "RFPL"},
        {"name": "Juan Cuadrado", "position": "FB", "club": "Atalanta", "club_league": "Serie A"},
        {"name": "David Ospina", "position": "GK", "club": "Al-Nassr", "club_league": "SPL"},
        {"name": "Johan Mojica", "position": "FB", "club": "Osasuna", "club_league": "La Liga"},
        {"name": "Yerson Mosquera", "position": "CB", "club": "Villarreal", "club_league": "La Liga"},
        {"name": "Deiver Machado", "position": "FB", "club": "Lens", "club_league": "Ligue 1"},
        {"name": "Jhon Lucumi", "position": "CB", "club": "Bologna", "club_league": "Serie A"},
        {"name": "Cristhian Mosquera", "position": "CB", "club": "Valencia", "club_league": "La Liga"},
        {"name": "Luis Muriel", "position": "ST", "club": "Orlando City", "club_league": "MLS"},
        {"name": "Mateus Uribe", "position": "CM", "club": "Al-Sadd", "club_league": "Qatar Stars League"},
        {"name": "Gustavo Cuellar", "position": "CM", "club": "Al-Shabab", "club_league": "SPL"},
        {"name": "Richard Rios", "position": "CM", "club": "Palmeiras", "club_league": "Brasileirao"},
        {"name": "Devis Vasquez", "position": "GK", "club": "Empoli", "club_league": "Serie A"},
        {"name": "Santiago Arias", "position": "FB", "club": "Bahia", "club_league": "Brasileirao"},
        {"name": "Miguel Borja", "position": "ST", "club": "River Plate", "club_league": "Liga Profesional"},
        {"name": "Kevin Castano", "position": "CM", "club": "Cruz Azul", "club_league": "Liga MX"},
        {"name": "Jorge Carrascal", "position": "AM", "club": "Dynamo Moscow", "club_league": "RFPL"},
        {"name": "Jhon Duran", "position": "ST", "club": "Aston Villa", "club_league": "Premier League"},
        {"name": "Yairo Moreno", "position": "FB", "club": "Leon", "club_league": "Liga MX"},
        {"name": "Jader Valencia", "position": "ST", "club": "Millonarios", "club_league": "Liga Profesional"},
    ],
    "Croatia": [
        {"name": "Dominik Livakovic", "position": "GK", "club": "Dinamo Zagreb", "club_league": "HNL"},
        {"name": "Josip Stanisic", "position": "FB", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Marin Pongracic", "position": "CB", "club": "Fiorentina", "club_league": "Serie A"},
        {"name": "Josko Gvardiol", "position": "CB", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Duje Caleta-Car", "position": "CB", "club": "Real Sociedad", "club_league": "La Liga"},
        {"name": "Josip Sutalo", "position": "CB", "club": "Ajax", "club_league": "Eredivisie"},
        {"name": "Nikola Moro", "position": "CM", "club": "Bologna", "club_league": "Serie A"},
        {"name": "Mateo Kovacic", "position": "CM", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Andrej Kramaric", "position": "ST", "club": "Hoffenheim", "club_league": "Bundesliga"},
        {"name": "Luka Modric", "position": "CM", "club": "AC Milan", "club_league": "Serie A"},
        {"name": "Ante Budimir", "position": "ST", "club": "Osasuna", "club_league": "La Liga"},
        {"name": "Ivor Pandur", "position": "GK", "club": "Hull City", "club_league": "EFL Championship"},
        {"name": "Nikola Vlasic", "position": "AM", "club": "Torino", "club_league": "Serie A"},
        {"name": "Ivan Perisic", "position": "W", "club": "PSV", "club_league": "Eredivisie"},
        {"name": "Mario Pasalic", "position": "AM", "club": "Atalanta", "club_league": "Serie A"},
        {"name": "Martin Baturina", "position": "AM", "club": "Como", "club_league": "Serie A"},
        {"name": "Petar Sucic", "position": "CM", "club": "Inter Milan", "club_league": "Serie A"},
        {"name": "Kristijan Jakic", "position": "DM", "club": "Augsburg", "club_league": "Bundesliga"},
        {"name": "Toni Fruk", "position": "CM", "club": "Rijeka", "club_league": "HNL"},
        {"name": "Igor Matanovic", "position": "ST", "club": "Freiburg", "club_league": "Bundesliga"},
        {"name": "Luka Sucic", "position": "AM", "club": "Real Sociedad", "club_league": "La Liga"},
        {"name": "Luka Vuskovic", "position": "CB", "club": "Hamburg", "club_league": "2. Bundesliga"},
        {"name": "Dominik Kotarski", "position": "GK", "club": "Copenhagen", "club_league": "Danish Superliga"},
        {"name": "Marco Pasalic", "position": "W", "club": "Orlando City", "club_league": "MLS"},
        {"name": "Martin Erlic", "position": "CB", "club": "Midtjylland", "club_league": "Danish Superliga"},
        {"name": "Petar Musa", "position": "ST", "club": "FC Dallas", "club_league": "MLS"},
    ],
    "Curacao": [
        {"name": "Eloy Room", "position": "GK", "club": "Miami FC", "club_league": "USL Championship"},
        {"name": "Shurandy Sambo", "position": "FB", "club": "Sparta Rotterdam", "club_league": "Eredivisie"},
        {"name": "Jurien Gaari", "position": "FB", "club": "Abha", "club_league": "SPL"},
        {"name": "Roshon van Eijma", "position": "CB", "club": "RKC Waalwijk", "club_league": "Eredivisie"},
        {"name": "Sherel Floranus", "position": "CB", "club": "PEC Zwolle", "club_league": "Eredivisie"},
        {"name": "Godfried Roemeratoe", "position": "CM", "club": "RKC Waalwijk", "club_league": "Eredivisie"},
        {"name": "Juninho Bacuna", "position": "CM", "club": "Volendam", "club_league": "Eredivisie"},
        {"name": "Livano Comenencia", "position": "CM", "club": "Zurich", "club_league": "Swiss Super League"},
        {"name": "Jurgen Locadia", "position": "ST", "club": "Miami FC", "club_league": "USL Championship"},
        {"name": "Leandro Bacuna", "position": "CM", "club": "Igdir", "club_league": "Super Lig"},
        {"name": "Jeremy Antonisse", "position": "W", "club": "Kifisia", "club_league": "Greek Super League"},
        {"name": "Misjonne Hansen", "position": "W", "club": "Middlesbrough", "club_league": "EFL Championship"},
        {"name": "Tyrese Noslin", "position": "W", "club": "Telstar", "club_league": "Eerste Divisie"},
        {"name": "Kenji Gorre", "position": "W", "club": "Maccabi Haifa", "club_league": "Israeli Premier League"},
        {"name": "Arjany Martha", "position": "CM", "club": "Rotherham United", "club_league": "EFL Championship"},
        {"name": "Jearl Margaritha", "position": "W", "club": "Beveren", "club_league": "Jupiler Pro League"},
        {"name": "Brandley Kuwas", "position": "W", "club": "Volendam", "club_league": "Eredivisie"},
        {"name": "Armando Obispo", "position": "CB", "club": "PSV", "club_league": "Eredivisie"},
        {"name": "Gervane Kastaneer", "position": "W", "club": "Terengganu", "club_league": "Malaysian Super League"},
        {"name": "Joshua Brenet", "position": "FB", "club": "Kayserispor", "club_league": "Super Lig"},
        {"name": "Tahith Chong", "position": "W", "club": "Sheffield United", "club_league": "EFL Championship"},
        {"name": "Kevin Felida", "position": "CM", "club": "Den Bosch", "club_league": "Eerste Divisie"},
        {"name": "Riechedly Bazoer", "position": "CB", "club": "Konyaspor", "club_league": "Super Lig"},
        {"name": "Deveron Fonville", "position": "CB", "club": "NEC Nijmegen", "club_league": "Eredivisie"},
        {"name": "Tyrick Bodak", "position": "GK", "club": "Telstar", "club_league": "Eerste Divisie"},
        {"name": "Trevor Doornbusch", "position": "GK", "club": "VVV Venlo", "club_league": "Eerste Divisie"},
    ],
    "Czech Republic": [
        {"name": "Matej Kovar", "position": "GK", "club": "PSV", "club_league": "Eredivisie"},
        {"name": "David Zima", "position": "CB", "club": "Slavia Prague", "club_league": "Czech First League"},
        {"name": "Tomas Holes", "position": "CB", "club": "Slavia Prague", "club_league": "Czech First League"},
        {"name": "Robin Hranac", "position": "CB", "club": "Hoffenheim", "club_league": "Bundesliga"},
        {"name": "Vladimir Coufal", "position": "FB", "club": "Hoffenheim", "club_league": "Bundesliga"},
        {"name": "Stepan Chaloupek", "position": "CB", "club": "Slavia Prague", "club_league": "Czech First League"},
        {"name": "Ladislav Krejci", "position": "FB", "club": "Girona", "club_league": "La Liga"},
        {"name": "Vladimir Darida", "position": "CM", "club": "PAOK", "club_league": "Greek Super League"},
        {"name": "Adam Hlozek", "position": "ST", "club": "Hoffenheim", "club_league": "Bundesliga"},
        {"name": "Patrik Schick", "position": "ST", "club": "Bayer Leverkusen", "club_league": "Bundesliga"},
        {"name": "Jan Kuchta", "position": "ST", "club": "Sparta Prague", "club_league": "Czech First League"},
        {"name": "Lukas Cerv", "position": "CM", "club": "Viktoria Plzen", "club_league": "Czech First League"},
        {"name": "Mojmir Chytil", "position": "ST", "club": "Slavia Prague", "club_league": "Czech First League"},
        {"name": "David Jurasek", "position": "FB", "club": "Slavia Prague", "club_league": "Czech First League"},
        {"name": "Pavel Sulc", "position": "ST", "club": "Lyon", "club_league": "Ligue 1"},
        {"name": "Jindrich Stanek", "position": "GK", "club": "Slavia Prague", "club_league": "Czech First League"},
        {"name": "Lukas Provod", "position": "CM", "club": "Slavia Prague", "club_league": "Czech First League"},
        {"name": "Michal Sadilek", "position": "CM", "club": "Slavia Prague", "club_league": "Czech First League"},
        {"name": "Tomas Chory", "position": "ST", "club": "Slavia Prague", "club_league": "Czech First League"},
        {"name": "Jaroslav Zeleny", "position": "FB", "club": "Slavia Prague", "club_league": "Czech First League"},
        {"name": "David Doudera", "position": "FB", "club": "Slavia Prague", "club_league": "Czech First League"},
        {"name": "Tomas Soucek", "position": "CM", "club": "West Ham", "club_league": "Premier League"},
        {"name": "Lukas Hornicek", "position": "GK", "club": "Braga", "club_league": "Liga Portugal"},
        {"name": "Alexandr Sojka", "position": "CM", "club": "Viktoria Plzen", "club_league": "Czech First League"},
        {"name": "Hugo Sochurek", "position": "CM", "club": "Viktoria Plzen", "club_league": "Czech First League"},
        {"name": "Denis Visinsky", "position": "ST", "club": "Viktoria Plzen", "club_league": "Czech First League"},
    ],
    "DR Congo": [
        {"name": "Cedric Makiadi", "position": "CM", "club": "Al-Fateh", "club_league": "SPL"},
        {"name": "Dieumerci Mbokani", "position": "ST", "club": "Kuwait SC", "club_league": "Kuwait Premier League"},
        {"name": "Yoane Wissa", "position": "W", "club": "Brentford", "club_league": "Premier League"},
        {"name": "Chancel Mbemba", "position": "CB", "club": "Marseille", "club_league": "Ligue 1"},
        {"name": "Arthur Masuaku", "position": "FB", "club": "Besiktas", "club_league": "Super Lig"},
        {"name": "Gaël Kakuta", "position": "AM", "club": "Lance", "club_league": "Ligue 1"},
        {"name": "Samuel Moutoussamy", "position": "CM", "club": "Nantes", "club_league": "Ligue 1"},
        {"name": "Silas Katompa Mvumpa", "position": "W", "club": "Stuttgart", "club_league": "Bundesliga"},
        {"name": "Jackson Muleka", "position": "ST", "club": "Besiktas", "club_league": "Super Lig"},
        {"name": "Oscar Mboza", "position": "CB", "club": "Lugano", "club_league": "Swiss Super League"},
        {"name": "Elikiya Mampuya", "position": "CB", "club": "LASK", "club_league": "Austrian Bundesliga"},
        {"name": "Christian Mawissa", "position": "FB", "club": "Monaco", "club_league": "Ligue 1"},
        {"name": "Aaron Tshibola", "position": "CM", "club": "Kilmarnock", "club_league": "Scottish Premiership"},
        {"name": "Ricky Tulenge", "position": "GK", "club": "Villarreal B", "club_league": "La Liga"},
        {"name": "Lionel Mpasi", "position": "GK", "club": "Rodez", "club_league": "Ligue 2"},
        {"name": "Patris Mbiakop", "position": "ST", "club": "Hapoel Beer Sheva", "club_league": "Israeli Premier League"},
        {"name": "Glody Ngonda", "position": "FB", "club": "Dijon", "club_league": "Ligue 2"},
        {"name": "Jacques Maghoma", "position": "W", "club": "Al-Ahli Tripoli", "club_league": "Libyan Premier League"},
        {"name": "Firmin Ndombe Mubele", "position": "W", "club": "Astana", "club_league": "Kazakhstan Premier League"},
        {"name": "Marcel Tisserand", "position": "CB", "club": "Al-Ittihad Kalba", "club_league": "UAE Pro League"},
        {"name": "William Balikwisha", "position": "W", "club": "OH Leuven", "club_league": "Jupiler Pro League"},
        {"name": "Meschak Elia", "position": "W", "club": "Young Boys", "club_league": "Swiss Super League"},
        {"name": "Jonathan Bolingi", "position": "ST", "club": "Al-Riffa", "club_league": "Bahrain Premier League"},
        {"name": "Paul-Jose M'Poku", "position": "W", "club": "Al-Fateh", "club_league": "SPL"},
        {"name": "Fabrice N'Sakala", "position": "FB", "club": "Besiktas", "club_league": "Super Lig"},
        {"name": "Jordan Botaka", "position": "W", "club": "Charleroi", "club_league": "Jupiler Pro League"},
    ],
    "Ecuador": [
        {"name": "Hernan Galindez", "position": "GK", "club": "Huracan", "club_league": "Liga Profesional"},
        {"name": "Felix Torres", "position": "CB", "club": "Internacional", "club_league": "Brasileirao"},
        {"name": "Piero Hincapie", "position": "CB", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Joel Ordonez", "position": "CB", "club": "Club Brugge", "club_league": "Jupiler Pro League"},
        {"name": "Jordy Alcivar", "position": "CM", "club": "Independiente del Valle", "club_league": "Liga Pro"},
        {"name": "Willian Pacho", "position": "CB", "club": "PSG", "club_league": "Ligue 1"},
        {"name": "Pervis Estupinan", "position": "FB", "club": "AC Milan", "club_league": "Serie A"},
        {"name": "Anthony Valencia", "position": "CM", "club": "Antwerp", "club_league": "Jupiler Pro League"},
        {"name": "John Yeboah", "position": "W", "club": "Venezia", "club_league": "Serie A"},
        {"name": "Kendry Paez", "position": "AM", "club": "River Plate", "club_league": "Liga Profesional"},
        {"name": "Kevin Rodriguez", "position": "ST", "club": "Imbabura", "club_league": "Liga Pro"},
        {"name": "Moises Ramirez", "position": "GK", "club": "Kifisia", "club_league": "Greek Super League"},
        {"name": "Enner Valencia", "position": "ST", "club": "Pachuca", "club_league": "Liga MX"},
        {"name": "Alan Minda", "position": "W", "club": "Atletico Mineiro", "club_league": "Brasileirao"},
        {"name": "Pedro Vite", "position": "CM", "club": "Pumas UNAM", "club_league": "Liga MX"},
        {"name": "Jordy Caicedo", "position": "ST", "club": "Huracan", "club_league": "Liga Profesional"},
        {"name": "Angelo Preciado", "position": "FB", "club": "Atletico Mineiro", "club_league": "Brasileirao"},
        {"name": "Denil Castillo", "position": "CM", "club": "Midtjylland", "club_league": "Danish Superliga"},
        {"name": "Gonzalo Plata", "position": "W", "club": "Flamengo", "club_league": "Brasileirao"},
        {"name": "Nilson Angulo", "position": "W", "club": "Sunderland", "club_league": "Premier League"},
        {"name": "Alan Franco", "position": "CM", "club": "Atletico Mineiro", "club_league": "Brasileirao"},
        {"name": "Gonzalo Valle", "position": "GK", "club": "Universidad Catolica", "club_league": "Liga Pro"},
        {"name": "Moises Caicedo", "position": "DM", "club": "Chelsea", "club_league": "Premier League"},
        {"name": "Jeremy Arevalo", "position": "ST", "club": "Stuttgart", "club_league": "Bundesliga"},
        {"name": "Jackson Porozo", "position": "CB", "club": "Tijuana", "club_league": "Liga MX"},
        {"name": "Yaimar Medina", "position": "CB", "club": "Genk", "club_league": "Jupiler Pro League"},
    ],
    "Egypt": [
        {"name": "Mohamed Elsayed", "position": "GK", "club": "Al Ahly", "club_league": "Egyptian Premier League"},
        {"name": "Yasser Ibrahim", "position": "CB", "club": "Al Ahly", "club_league": "Egyptian Premier League"},
        {"name": "Mohamed Hany", "position": "CB", "club": "Al Ahly", "club_league": "Egyptian Premier League"},
        {"name": "Hossam Abdelmegeed", "position": "CB", "club": "Zamalek", "club_league": "Egyptian Premier League"},
        {"name": "Ramy Hisham", "position": "CB", "club": "Al Ain", "club_league": "UAE Pro League"},
        {"name": "Mohamed Abdelmoneim", "position": "CB", "club": "Nice", "club_league": "Ligue 1"},
        {"name": "Mahmoud Ahmed Ibrahim", "position": "ST", "club": "Al Ahly", "club_league": "Egyptian Premier League"},
        {"name": "Emam Ashour", "position": "AM", "club": "Al Ahly", "club_league": "Egyptian Premier League"},
        {"name": "Hamza Abdelkarim", "position": "W", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Mohamed Salah", "position": "W", "club": "Liverpool", "club_league": "Premier League"},
        {"name": "Mostafa Mohamed Zaky", "position": "CM", "club": "Pyramids", "club_league": "Egyptian Premier League"},
        {"name": "Haissem Yousry", "position": "W", "club": "Real Oviedo", "club_league": "La Liga"},
        {"name": "Ahmed Aboelfetouh", "position": "FB", "club": "Zamalek", "club_league": "Egyptian Premier League"},
        {"name": "Hamdy Fathy", "position": "CM", "club": "Al Wakrah", "club_league": "Qatar Stars League"},
        {"name": "Karim Hafez", "position": "CB", "club": "Pyramids", "club_league": "Egyptian Premier League"},
        {"name": "Mahdy Soliman", "position": "GK", "club": "Zamalek", "club_league": "Egyptian Premier League"},
        {"name": "Mohanad Mostafa", "position": "CM", "club": "Pyramids", "club_league": "Egyptian Premier League"},
        {"name": "Nabil Emad", "position": "CM", "club": "Al Najmah", "club_league": "SPL"},
        {"name": "Marawan Attia", "position": "CM", "club": "Al Ahly", "club_league": "Egyptian Premier League"},
        {"name": "Ibrahim Adel", "position": "W", "club": "Nordsjaelland", "club_league": "Danish Superliga"},
        {"name": "Mahmoud Saber", "position": "CM", "club": "ZED FC", "club_league": "Egyptian Premier League"},
        {"name": "Omar Marmoush", "position": "ST", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Mostafa Abdelaziz", "position": "GK", "club": "Al Ahly", "club_league": "Egyptian Premier League"},
        {"name": "Tarek Alaa", "position": "CB", "club": "ZED FC", "club_league": "Egyptian Premier League"},
        {"name": "Ahmed Mostafa", "position": "ST", "club": "Al Ahly", "club_league": "Egyptian Premier League"},
        {"name": "Mohamed Alaaeldin", "position": "GK", "club": "El Gouna", "club_league": "Egyptian Premier League"},
    ],
    "England": [
        {"name": "Jordan Pickford", "position": "GK", "club": "Everton", "club_league": "Premier League"},
        {"name": "Dean Henderson", "position": "GK", "club": "Crystal Palace", "club_league": "Premier League"},
        {"name": "James Trafford", "position": "GK", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Reece James", "position": "FB", "club": "Chelsea", "club_league": "Premier League"},
        {"name": "Tino Livramento", "position": "FB", "club": "Newcastle United", "club_league": "Premier League"},
        {"name": "Djed Spence", "position": "FB", "club": "Tottenham", "club_league": "Premier League"},
        {"name": "Marc Guehi", "position": "CB", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "John Stones", "position": "CB", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Ezri Konsa", "position": "CB", "club": "Aston Villa", "club_league": "Premier League"},
        {"name": "Jarell Quansah", "position": "CB", "club": "Bayer Leverkusen", "club_league": "Bundesliga"},
        {"name": "Dan Burn", "position": "CB", "club": "Newcastle United", "club_league": "Premier League"},
        {"name": "Nico O'Reilly", "position": "CB", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Declan Rice", "position": "CM", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Jordan Henderson", "position": "CM", "club": "Brentford", "club_league": "Premier League"},
        {"name": "Kobbie Mainoo", "position": "CM", "club": "Manchester United", "club_league": "Premier League"},
        {"name": "Elliot Anderson", "position": "CM", "club": "Nottingham Forest", "club_league": "Premier League"},
        {"name": "Jude Bellingham", "position": "AM", "club": "Real Madrid", "club_league": "La Liga"},
        {"name": "Morgan Rogers", "position": "AM", "club": "Aston Villa", "club_league": "Premier League"},
        {"name": "Eberechi Eze", "position": "AM", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Harry Kane", "position": "ST", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Ivan Toney", "position": "ST", "club": "Al Ahli", "club_league": "SPL"},
        {"name": "Ollie Watkins", "position": "ST", "club": "Aston Villa", "club_league": "Premier League"},
        {"name": "Bukayo Saka", "position": "W", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Marcus Rashford", "position": "W", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Noni Madueke", "position": "W", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Anthony Gordon", "position": "W", "club": "Newcastle United", "club_league": "Premier League"},
    ],
    "France": [
        {"name": "Brice Samba", "position": "GK", "club": "Rennes", "club_league": "Ligue 1"},
        {"name": "Malo Gusto", "position": "FB", "club": "Chelsea", "club_league": "Premier League"},
        {"name": "Lucas Digne", "position": "FB", "club": "Aston Villa", "club_league": "Premier League"},
        {"name": "Dayot Upamecano", "position": "CB", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Jules Kounde", "position": "CB", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Manu Kone", "position": "CM", "club": "Roma", "club_league": "Serie A"},
        {"name": "Ousmane Dembele", "position": "W", "club": "Paris Saint-Germain", "club_league": "Ligue 1"},
        {"name": "Aurelien Tchouameni", "position": "DM", "club": "Real Madrid", "club_league": "La Liga"},
        {"name": "Marcus Thuram", "position": "ST", "club": "Inter Milan", "club_league": "Serie A"},
        {"name": "Kylian Mbappe", "position": "ST", "club": "Real Madrid", "club_league": "La Liga"},
        {"name": "Michael Olise", "position": "W", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Bradley Barcola", "position": "W", "club": "Paris Saint-Germain", "club_league": "Ligue 1"},
        {"name": "N'Golo Kante", "position": "DM", "club": "Fenerbahce", "club_league": "Super Lig"},
        {"name": "Adrien Rabiot", "position": "CM", "club": "AC Milan", "club_league": "Serie A"},
        {"name": "Ibrahima Konate", "position": "CB", "club": "Liverpool", "club_league": "Premier League"},
        {"name": "Mike Maignan", "position": "GK", "club": "AC Milan", "club_league": "Serie A"},
        {"name": "William Saliba", "position": "CB", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Warren Zaire-Emery", "position": "CM", "club": "Paris Saint-Germain", "club_league": "Ligue 1"},
        {"name": "Theo Hernandez", "position": "FB", "club": "Al Hilal", "club_league": "SPL"},
        {"name": "Desire Doue", "position": "W", "club": "Paris Saint-Germain", "club_league": "Ligue 1"},
        {"name": "Lucas Hernandez", "position": "CB", "club": "Paris Saint-Germain", "club_league": "Ligue 1"},
        {"name": "Jean-Philippe Mateta", "position": "ST", "club": "Crystal Palace", "club_league": "Premier League"},
        {"name": "Robin Risser", "position": "GK", "club": "Lens", "club_league": "Ligue 1"},
        {"name": "Rayan Cherki", "position": "AM", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Maghnes Akliouche", "position": "AM", "club": "Monaco", "club_league": "Ligue 1"},
        {"name": "Maxence Lacroix", "position": "CB", "club": "Crystal Palace", "club_league": "Premier League"},
    ],
    "Germany": [
        {"name": "Manuel Neuer", "position": "GK", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Antonio Rudiger", "position": "CB", "club": "Real Madrid", "club_league": "La Liga"},
        {"name": "Waldemar Anton", "position": "CB", "club": "Borussia Dortmund", "club_league": "Bundesliga"},
        {"name": "Jonathan Tah", "position": "CB", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Aleksandar Pavlovic", "position": "CM", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Joshua Kimmich", "position": "FB", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Kai Havertz", "position": "ST", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Leon Goretzka", "position": "CM", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Jamie Leweling", "position": "W", "club": "Stuttgart", "club_league": "Bundesliga"},
        {"name": "Jamal Musiala", "position": "AM", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Nick Woltemade", "position": "ST", "club": "Newcastle United", "club_league": "Premier League"},
        {"name": "Oliver Baumann", "position": "GK", "club": "Hoffenheim", "club_league": "Bundesliga"},
        {"name": "Pascal Gross", "position": "CM", "club": "Brighton", "club_league": "Premier League"},
        {"name": "Maximilian Beier", "position": "ST", "club": "Borussia Dortmund", "club_league": "Bundesliga"},
        {"name": "Nico Schlotterbeck", "position": "CB", "club": "Borussia Dortmund", "club_league": "Bundesliga"},
        {"name": "Angelo Stiller", "position": "CM", "club": "Stuttgart", "club_league": "Bundesliga"},
        {"name": "Florian Wirtz", "position": "AM", "club": "Liverpool", "club_league": "Premier League"},
        {"name": "Nathaniel Brown", "position": "CB", "club": "Eintracht Frankfurt", "club_league": "Bundesliga"},
        {"name": "Leroy Sane", "position": "W", "club": "Galatasaray", "club_league": "Super Lig"},
        {"name": "Nadiem Amiri", "position": "CM", "club": "Mainz 05", "club_league": "Bundesliga"},
        {"name": "Alexander Nubel", "position": "GK", "club": "Stuttgart", "club_league": "Bundesliga"},
        {"name": "David Raum", "position": "FB", "club": "RB Leipzig", "club_league": "Bundesliga"},
        {"name": "Felix Nmecha", "position": "CM", "club": "Borussia Dortmund", "club_league": "Bundesliga"},
        {"name": "Malick Thiaw", "position": "CB", "club": "Newcastle United", "club_league": "Premier League"},
        {"name": "Lennart Karl", "position": "CM", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Deniz Undav", "position": "ST", "club": "Stuttgart", "club_league": "Bundesliga"},
    ],
    "Ghana": [
        {"name": "Lawrence Ati-Zigi", "position": "GK", "club": "St. Gallen", "club_league": "Swiss Super League"},
        {"name": "Alidu", "position": "CB", "club": "Rennes", "club_league": "Ligue 1"},
        {"name": "Caleb Marfo", "position": "CM", "club": "Nordsjaelland", "club_league": "Danish Superliga"},
        {"name": "Jonas Adjei", "position": "CB", "club": "Wolfsburg", "club_league": "Bundesliga"},
        {"name": "Thomas Partey", "position": "CM", "club": "Villarreal", "club_league": "La Liga"},
        {"name": "Abdul Mumin", "position": "CB", "club": "Rayo Vallecano", "club_league": "La Liga"},
        {"name": "Abdul Fatawu", "position": "W", "club": "Leicester", "club_league": "Premier League"},
        {"name": "Kwasi", "position": "CM", "club": "Real Oviedo", "club_league": "La Liga"},
        {"name": "Jordan Ayew", "position": "ST", "club": "Leicester", "club_league": "Premier League"},
        {"name": "Solomon Clarke", "position": "ST", "club": "Coventry City", "club_league": "EFL Championship"},
        {"name": "Antoine Semenyo", "position": "CM", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Joseph Tetteh", "position": "GK", "club": "St Patrick's Athletic", "club_league": "League of Ireland"},
        {"name": "Christopher Bonsu", "position": "ST", "club": "Al Qadsiah", "club_league": "SPL"},
        {"name": "Gideon", "position": "CB", "club": "Auxerre", "club_league": "Ligue 1"},
        {"name": "Elisha", "position": "CM", "club": "Auxerre", "club_league": "Ligue 1"},
        {"name": "Benjamin", "position": "GK", "club": "Hearts of Oak", "club_league": "Ghana Premier League"},
        {"name": "Abdul Rahaman", "position": "CB", "club": "PAOK", "club_league": "Greek Super League"},
        {"name": "Jerome", "position": "CB", "club": "Basaksehir", "club_league": "Super Lig"},
        {"name": "Inaki Williams", "position": "ST", "club": "Athletic Bilbao", "club_league": "La Liga"},
        {"name": "Augustine", "position": "CM", "club": "Saint-Etienne", "club_league": "Ligue 1"},
        {"name": "Kojo Peprah", "position": "CB", "club": "Nice", "club_league": "Ligue 1"},
        {"name": "Kamal Deen", "position": "W", "club": "Atalanta", "club_league": "Serie A"},
        {"name": "Derrick", "position": "CB", "club": "Pafos", "club_league": "Cypriot First Division"},
        {"name": "Ernest Nuamah", "position": "W", "club": "Lyon", "club_league": "Ligue 1"},
        {"name": "Prince Kwabena", "position": "ST", "club": "Viktoria Plzen", "club_league": "Czech First League"},
        {"name": "Marvin Elom", "position": "CB", "club": "Auxerre", "club_league": "Ligue 1"},
    ],
    "Haiti": [
        {"name": "Johny Placide", "position": "GK", "club": "Bastia", "club_league": "Ligue 2"},
        {"name": "Carlens Arcus", "position": "FB", "club": "Angers", "club_league": "Ligue 1"},
        {"name": "Keeto Thermoncy", "position": "CB", "club": "Young Boys", "club_league": "Swiss Super League"},
        {"name": "Ricardo Ade", "position": "CB", "club": "Universidad Catolica", "club_league": "Liga Pro"},
        {"name": "Hannes Delcroix", "position": "CB", "club": "Lugano", "club_league": "Swiss Super League"},
        {"name": "Carl Fred Sainte", "position": "CM", "club": "El Paso Locomotive", "club_league": "USL Championship"},
        {"name": "Derrick Etienne Jr", "position": "W", "club": "Toronto FC", "club_league": "MLS"},
        {"name": "Martin Experience", "position": "CB", "club": "Nancy", "club_league": "National 1"},
        {"name": "Duckens Nazon", "position": "ST", "club": "Esteghlal Tehran", "club_league": "Persian Gulf Pro League"},
        {"name": "Jean-Ricner Bellegarde", "position": "CM", "club": "Wolverhampton", "club_league": "Premier League"},
        {"name": "Don Deedson Louicius", "position": "ST", "club": "FC Dallas", "club_league": "MLS"},
        {"name": "Alexandre Pierre", "position": "GK", "club": "Sochaux", "club_league": "National 1"},
        {"name": "Markhus Lacroix", "position": "CB", "club": "Colorado Springs Switchbacks", "club_league": "USL Championship"},
        {"name": "Garven-Michee Metusala", "position": "CB", "club": "Free Agent", "club_league": "Unknown"},
        {"name": "Ruben Providence", "position": "W", "club": "Almere City", "club_league": "Eredivisie"},
        {"name": "Lenny Joseph", "position": "ST", "club": "Ferencvaros", "club_league": "NB I"},
        {"name": "Danley Jean Jacques", "position": "CM", "club": "Philadelphia Union", "club_league": "MLS"},
        {"name": "Wilson Isidor", "position": "ST", "club": "Sunderland", "club_league": "Premier League"},
        {"name": "Yassin Fortune", "position": "W", "club": "Vizela", "club_league": "Liga Portugal 2"},
        {"name": "Frantzdy Pierrot", "position": "ST", "club": "Rizespor", "club_league": "Super Lig"},
        {"name": "Josue Casimir", "position": "CM", "club": "Auxerre", "club_league": "Ligue 1"},
        {"name": "Jean-Kevin Duverne", "position": "CB", "club": "Gent", "club_league": "Jupiler Pro League"},
        {"name": "Josue Duverger", "position": "GK", "club": "Free Agent", "club_league": "Unknown"},
        {"name": "Wilguens Paugain", "position": "CB", "club": "Beerschot", "club_league": "Jupiler Pro League"},
        {"name": "Dominique Simon", "position": "CM", "club": "Presov", "club_league": "2. Liga"},
        {"name": "Olivier Pierre", "position": "CM", "club": "Real Hope", "club_league": "Ligue Haitienne"},
    ],
    "Iran": [
        {"name": "Alireza Safarbeiranvand", "position": "GK", "club": "Tractor", "club_league": "Persian Gulf Pro League"},
        {"name": "Saleh Hardani", "position": "CB", "club": "Esteghlal", "club_league": "Persian Gulf Pro League"},
        {"name": "Ehsan Hajsafi", "position": "CB", "club": "Sepahan", "club_league": "Persian Gulf Pro League"},
        {"name": "Shojae Khalilzadeh", "position": "CB", "club": "Tractor", "club_league": "Persian Gulf Pro League"},
        {"name": "Milad Mohammadi", "position": "CB", "club": "Persepolis", "club_league": "Persian Gulf Pro League"},
        {"name": "Saeid Ezatolahi", "position": "CM", "club": "Shabab Al Ahli", "club_league": "UAE Pro League"},
        {"name": "Alireza Jahanbakhsh", "position": "CM", "club": "Dender", "club_league": "Jupiler Pro League"},
        {"name": "Mohammad Mohebbi", "position": "CM", "club": "Rostov", "club_league": "RFPL"},
        {"name": "Mehdi Taremi", "position": "ST", "club": "Olympiacos", "club_league": "Greek Super League"},
        {"name": "Mehdi Ghayedi", "position": "W", "club": "Al Nasr", "club_league": "UAE Pro League"},
        {"name": "Ali Alipourghara", "position": "ST", "club": "Persepolis", "club_league": "Persian Gulf Pro League"},
        {"name": "Seyedpayam Niazmand", "position": "GK", "club": "Persepolis", "club_league": "Persian Gulf Pro League"},
        {"name": "Mohammadhossein Kanani", "position": "CB", "club": "Persepolis", "club_league": "Persian Gulf Pro League"},
        {"name": "Saman Ghoddos", "position": "AM", "club": "Ittihad Kalba", "club_league": "UAE Pro League"},
        {"name": "Roozbeh Cheshmi", "position": "CM", "club": "Esteghlal", "club_league": "Persian Gulf Pro League"},
        {"name": "Mahdi Torabi", "position": "CM", "club": "Tractor", "club_league": "Persian Gulf Pro League"},
        {"name": "Arya Yousefi", "position": "CB", "club": "Sepahan", "club_league": "Persian Gulf Pro League"},
        {"name": "Amirhossein Hosseinzadeh", "position": "ST", "club": "Tractor", "club_league": "Persian Gulf Pro League"},
        {"name": "Ali Nemati", "position": "CB", "club": "Foolad", "club_league": "Persian Gulf Pro League"},
        {"name": "Shahriyar Moghanloo", "position": "ST", "club": "Ittihad Kalba", "club_league": "UAE Pro League"},
        {"name": "Mohammad Ghorbani", "position": "CM", "club": "Al Wahda", "club_league": "UAE Pro League"},
        {"name": "Seyedhossein Hosseini", "position": "GK", "club": "Sepahan", "club_league": "Persian Gulf Pro League"},
        {"name": "Ramin Rezaeian", "position": "FB", "club": "Foolad", "club_league": "Persian Gulf Pro League"},
        {"name": "Dennis Dargahi", "position": "ST", "club": "Standard Liege", "club_league": "Jupiler Pro League"},
        {"name": "Danial Iri", "position": "CB", "club": "Malavan", "club_league": "Persian Gulf Pro League"},
        {"name": "Amirmohammad Razaghinia", "position": "CM", "club": "Esteghlal", "club_league": "Persian Gulf Pro League"},
    ],
    "Iraq": [
        {"name": "Fahad Raheem", "position": "GK", "club": "Al Talaba", "club_league": "Iraqi Premier League"},
        {"name": "Rebin Solaka", "position": "CB", "club": "Port FC", "club_league": "Thai League 1"},
        {"name": "Hussein Ali", "position": "CB", "club": "Pogon Szczecin", "club_league": "Ekstraklasa"},
        {"name": "Zaid Hantoosh", "position": "CB", "club": "Pakhtakor", "club_league": "Uzbekistan Super League"},
        {"name": "Akam Rahman", "position": "CB", "club": "Al Zawraa", "club_league": "Iraqi Premier League"},
        {"name": "Munaf Al-Tekreeti", "position": "CB", "club": "Al Shorta", "club_league": "Iraqi Premier League"},
        {"name": "Youssef Amyn", "position": "CM", "club": "AEK Larnaca", "club_league": "Cypriot First Division"},
        {"name": "Ibrahim Bayesh", "position": "CM", "club": "Al Dhafra", "club_league": "UAE Pro League"},
        {"name": "Ali Alzubaidi", "position": "W", "club": "Luton Town", "club_league": "EFL Championship"},
        {"name": "Mohanad Ali", "position": "ST", "club": "Dibba", "club_league": "UAE Pro League"},
        {"name": "Ahmed Ahmed", "position": "ST", "club": "Nashville SC", "club_league": "MLS"},
        {"name": "Jalal Hachim", "position": "GK", "club": "Al Zawraa", "club_league": "Iraqi Premier League"},
        {"name": "Ali Najatee", "position": "ST", "club": "Al Talaba", "club_league": "Iraqi Premier League"},
        {"name": "Zidane Iqbal", "position": "CM", "club": "Utrecht", "club_league": "Eredivisie"},
        {"name": "Ahmed Al-Deeshawee", "position": "CB", "club": "Al Karma", "club_league": "Iraqi Premier League"},
        {"name": "Amir Al-Ammari", "position": "CM", "club": "Cracovia", "club_league": "Ekstraklasa"},
        {"name": "Ali Jasim", "position": "ST", "club": "Al Najmah", "club_league": "SPL"},
        {"name": "Aymen Hussein", "position": "ST", "club": "Al Karma", "club_league": "Iraqi Premier League"},
        {"name": "Kevin William", "position": "CM", "club": "AGF Aarhus", "club_league": "Danish Superliga"},
        {"name": "Aimar Sher", "position": "CM", "club": "Sarpsborg 08", "club_league": "Eliteserien"},
        {"name": "Marko Hussein", "position": "ST", "club": "Venezia", "club_league": "Serie A"},
        {"name": "Ahmed Al-Fadhli", "position": "GK", "club": "Al Shorta", "club_league": "Iraqi Premier League"},
        {"name": "Merchas Salih", "position": "CB", "club": "Viktoria Plzen", "club_league": "Czech First League"},
        {"name": "Zaid Al-Dulaimi", "position": "CM", "club": "Al Talaba", "club_league": "Iraqi Premier League"},
        {"name": "Mustafa Al Korji", "position": "CB", "club": "Al Shorta", "club_league": "Iraqi Premier League"},
        {"name": "Frans Haddad", "position": "CB", "club": "Persib Bandung", "club_league": "Liga 1"},
    ],
    "Ivory Coast": [
        {"name": "Nicolas Pepe", "position": "W", "club": "Trabzonspor", "club_league": "Super Lig"},
        {"name": "Serge Aurier", "position": "FB", "club": "Galatasaray", "club_league": "Super Lig"},
        {"name": "Franck Kessie", "position": "CM", "club": "Al-Ahli", "club_league": "SPL"},
        {"name": "Wilfried Zaha", "position": "W", "club": "Galatasaray", "club_league": "Super Lig"},
        {"name": "Eric Bailly", "position": "CB", "club": "Besiktas", "club_league": "Super Lig"},
        {"name": "Jean Michael Seri", "position": "CM", "club": "Hull City", "club_league": "EFL Championship"},
        {"name": "Ibrahim Sangare", "position": "CM", "club": "Nottingham Forest", "club_league": "Premier League"},
        {"name": "Simon Deli", "position": "CB", "club": "Adana Demirspor", "club_league": "Super Lig"},
        {"name": "Seko Fofana", "position": "CM", "club": "Al-Ettifaq", "club_league": "SPL"},
        {"name": "Ousmane Diomande", "position": "CB", "club": "Sporting CP", "club_league": "Liga Portugal"},
        {"name": "Jeremie Boga", "position": "W", "club": "Nice", "club_league": "Ligue 1"},
        {"name": "Christian Kouame", "position": "W", "club": "Fiorentina", "club_league": "Serie A"},
        {"name": "Sebastien Haller", "position": "ST", "club": "Leverkusen", "club_league": "Bundesliga"},
        {"name": "Jonathan Bamba", "position": "W", "club": "Celta Vigo", "club_league": "La Liga"},
        {"name": "Maxwel Cornet", "position": "W", "club": "Genoa", "club_league": "Serie A"},
        {"name": "Odilon Kossounou", "position": "CB", "club": "Atalanta", "club_league": "Serie A"},
        {"name": "Evan Ndicka", "position": "CB", "club": "Roma", "club_league": "Serie A"},
        {"name": "Serge Gnonto", "position": "W", "club": "Ivory Coast NT", "club_league": "Other"},
        {"name": "Yahia Fofana", "position": "GK", "club": "Angers", "club_league": "Ligue 1"},
        {"name": "Badra Ali Sangare", "position": "GK", "club": "JDT", "club_league": "Malaysian Super League"},
        {"name": "Karl Toko Ekambi", "position": "W", "club": "Al-Duhail", "club_league": "Qatar Stars League"},
        {"name": "Lazare Amani", "position": "AM", "club": "Union SG", "club_league": "Jupiler Pro League"},
        {"name": "Ghislain Konan", "position": "FB", "club": "Al-Fayha", "club_league": "SPL"},
        {"name": "Wilfried Singo", "position": "FB", "club": "Monaco", "club_league": "Ligue 1"},
        {"name": "Moussa Niakhate", "position": "CB", "club": "Lyon", "club_league": "Ligue 1"},
        {"name": "Hamed Traore", "position": "AM", "club": "Bournemouth", "club_league": "Premier League"},
    ],
    "Japan": [
        {"name": "Zion Suzuki", "position": "GK", "club": "Parma", "club_league": "Serie A"},
        {"name": "Yukinari Sugawara", "position": "FB", "club": "Werder Bremen", "club_league": "Bundesliga"},
        {"name": "Shogo Taniguchi", "position": "CB", "club": "Sint-Truiden", "club_league": "Jupiler Pro League"},
        {"name": "Kou Itakura", "position": "CB", "club": "Ajax", "club_league": "Eredivisie"},
        {"name": "Yuto Nagatomo", "position": "FB", "club": "FC Tokyo", "club_league": "J-League"},
        {"name": "Shuto Machino", "position": "ST", "club": "Holstein Kiel", "club_league": "Bundesliga"},
        {"name": "Ao Tanaka", "position": "CM", "club": "Leeds United", "club_league": "Premier League"},
        {"name": "Takefusa Kubo", "position": "AM", "club": "Real Sociedad", "club_league": "La Liga"},
        {"name": "Keisuke Goto", "position": "ST", "club": "Sint-Truiden", "club_league": "Jupiler Pro League"},
        {"name": "Ritsu Doan", "position": "CM", "club": "Ein Frankfurt", "club_league": "Bundesliga"},
        {"name": "Daizen Maeda", "position": "W", "club": "Celtic", "club_league": "Scottish Premiership"},
        {"name": "Keisuke Osako", "position": "GK", "club": "Sanfrecce Hiroshima", "club_league": "J-League"},
        {"name": "Keito Nakamura", "position": "W", "club": "Reims", "club_league": "Ligue 1"},
        {"name": "Junya Ito", "position": "W", "club": "Genk", "club_league": "Jupiler Pro League"},
        {"name": "Daichi Kamada", "position": "CM", "club": "Crystal Palace", "club_league": "Premier League"},
        {"name": "Tsuyoshi Watanabe", "position": "CB", "club": "Feyenoord", "club_league": "Eredivisie"},
        {"name": "Yuito Suzuki", "position": "CM", "club": "Freiburg", "club_league": "Bundesliga"},
        {"name": "Ayase Ueda", "position": "ST", "club": "Feyenoord", "club_league": "Eredivisie"},
        {"name": "Koki Ogawa", "position": "ST", "club": "NEC Nijmegen", "club_league": "Eredivisie"},
        {"name": "Ayumu Seko", "position": "CB", "club": "Le Havre", "club_league": "Ligue 1"},
        {"name": "Hiroki Ito", "position": "CB", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Takehiro Tomiyasu", "position": "CB", "club": "Ajax", "club_league": "Eredivisie"},
        {"name": "Tomoki Hayakawa", "position": "GK", "club": "Kashima Antlers", "club_league": "J-League"},
        {"name": "Kaishu Sano", "position": "CM", "club": "Mainz 05", "club_league": "Bundesliga"},
        {"name": "Junnosuke Suzuki", "position": "CB", "club": "Copenhagen", "club_league": "Danish Superliga"},
        {"name": "Kento Shiogai", "position": "W", "club": "Wolfsburg", "club_league": "Bundesliga"},
    ],
    "Jordan": [
        {"name": "Yazeed Abunada", "position": "GK", "club": "Al Hussein SC", "club_league": "Jordanian Pro League"},
        {"name": "Mohammad Ali Hasan", "position": "CB", "club": "Al Karma SC", "club_league": "Iraqi Premier League"},
        {"name": "Abdallah Mousa", "position": "CB", "club": "Al Zawraa SC", "club_league": "Iraqi Premier League"},
        {"name": "Husam Ali", "position": "CB", "club": "Al Faisaly SC", "club_league": "Jordanian Pro League"},
        {"name": "Yazan Mahmoud", "position": "CB", "club": "FC Seoul", "club_league": "K League 1"},
        {"name": "Amer Rasem", "position": "CM", "club": "Al Zawraa SC", "club_league": "Iraqi Premier League"},
        {"name": "Mohammad Faisal", "position": "ST", "club": "Raja Casablanca", "club_league": "Botola Pro"},
        {"name": "Noor Al-Deen Mahmoud", "position": "CM", "club": "Selangor FC", "club_league": "Malaysian Super League"},
        {"name": "Ali Iyad", "position": "ST", "club": "Al Sailiya SC", "club_league": "Qatar Stars League"},
        {"name": "Mousa Mohammad", "position": "ST", "club": "Rennes", "club_league": "Ligue 1"},
        {"name": "Odeh Shehadeh", "position": "ST", "club": "Pyramids FC", "club_league": "Egyptian Premier League"},
        {"name": "Noureddin Khaleel", "position": "GK", "club": "Al Faisaly SC", "club_league": "Jordanian Pro League"},
        {"name": "Mahmoud Nayef", "position": "ST", "club": "Al Hussein SC", "club_league": "Jordanian Pro League"},
        {"name": "Raja'i Ayed", "position": "CM", "club": "Al Hussein SC", "club_league": "Jordanian Pro League"},
        {"name": "Ibrahim Sami", "position": "CM", "club": "Al Karma SC", "club_league": "Iraqi Premier League"},
        {"name": "Mohammad Majed", "position": "FB", "club": "Selangor FC", "club_league": "Malaysian Super League"},
        {"name": "Saleem Amer", "position": "CB", "club": "Al Hussein SC", "club_league": "Jordanian Pro League"},
        {"name": "Mohammad Ahmed", "position": "CM", "club": "Al Hussein SC", "club_league": "Jordanian Pro League"},
        {"name": "Sa'ed Salameh", "position": "CB", "club": "Al Hussein SC", "club_league": "Jordanian Pro League"},
        {"name": "Mohannad Saleh", "position": "CM", "club": "Al-Quwa Al-Jawiya", "club_league": "Iraqi Premier League"},
        {"name": "Nizar Ahmed", "position": "CM", "club": "Qatar SC", "club_league": "Qatar Stars League"},
        {"name": "Abdallah Mahmoud", "position": "GK", "club": "Al Wahdat SC", "club_league": "Jordanian Pro League"},
        {"name": "Ehsan Farhan", "position": "CB", "club": "Al Hussein SC", "club_league": "Jordanian Pro League"},
        {"name": "Ali Ahmad", "position": "ST", "club": "Al Shabab FC", "club_league": "SPL"},
        {"name": "Mohammad Ratib", "position": "CM", "club": "Al Wahdat SC", "club_league": "Jordanian Pro League"},
        {"name": "Anas Ghazi", "position": "CB", "club": "Al Faisaly SC", "club_league": "Jordanian Pro League"},
    ],
    "Mexico": [
        {"name": "Jose Rangel", "position": "GK", "club": "Guadalajara", "club_league": "Liga MX"},
        {"name": "Jorge Sanchez", "position": "FB", "club": "PAOK", "club_league": "Super League"},
        {"name": "Cesar Montes", "position": "CB", "club": "Lokomotiv Moscow", "club_league": "RFPL"},
        {"name": "Edson Alvarez", "position": "CB", "club": "Fenerbahce", "club_league": "Super Lig"},
        {"name": "Johan Vasquez", "position": "CB", "club": "Genoa", "club_league": "Serie A"},
        {"name": "Erik Lira", "position": "CM", "club": "Cruz Azul", "club_league": "Liga MX"},
        {"name": "Luis Romo", "position": "CM", "club": "Guadalajara", "club_league": "Liga MX"},
        {"name": "Alvaro Fidalgo", "position": "CM", "club": "Real Betis", "club_league": "La Liga"},
        {"name": "Raul Jimenez", "position": "ST", "club": "Fulham", "club_league": "Premier League"},
        {"name": "Alexis Vega", "position": "W", "club": "Toluca", "club_league": "Liga MX"},
        {"name": "Santiago Gimenez", "position": "ST", "club": "AC Milan", "club_league": "Serie A"},
        {"name": "Carlos Acevedo", "position": "GK", "club": "Santos Laguna", "club_league": "Liga MX"},
        {"name": "Guillermo Ochoa", "position": "GK", "club": "AEL Limassol", "club_league": "Cypriot First Division"},
        {"name": "Armando Gonzalez", "position": "ST", "club": "Guadalajara", "club_league": "Liga MX"},
        {"name": "Israel Reyes", "position": "CB", "club": "Club America", "club_league": "Liga MX"},
        {"name": "Julian Quinones", "position": "W", "club": "Al Qadsiah", "club_league": "SPL"},
        {"name": "Orbelin Pineda", "position": "CM", "club": "AEK Athens", "club_league": "Super League"},
        {"name": "Obed Vargas", "position": "CM", "club": "Atletico Madrid", "club_league": "La Liga"},
        {"name": "Gilberto Mora", "position": "CM", "club": "Club Tijuana", "club_league": "Liga MX"},
        {"name": "Mateo Chavez", "position": "FB", "club": "AZ Alkmaar", "club_league": "Eredivisie"},
        {"name": "Cesar Huerta", "position": "W", "club": "Anderlecht", "club_league": "Jupiler Pro League"},
        {"name": "Guillermo Martinez", "position": "ST", "club": "Pumas UNAM", "club_league": "Liga MX"},
        {"name": "Jesus Gallardo", "position": "FB", "club": "Toluca", "club_league": "Liga MX"},
        {"name": "Luis Chavez", "position": "CM", "club": "Dynamo Moscow", "club_league": "RFPL"},
        {"name": "Roberto Alvarado", "position": "W", "club": "Guadalajara", "club_league": "Liga MX"},
        {"name": "Brian Gutierrez", "position": "CM", "club": "Guadalajara", "club_league": "Liga MX"},
    ],
    "Morocco": [
        {"name": "Achraf Hakimi", "position": "FB", "club": "PSG", "club_league": "Ligue 1"},
        {"name": "Sofyan Amrabat", "position": "CM", "club": "Fenerbahce", "club_league": "Super Lig"},
        {"name": "Nayef Aguerd", "position": "CB", "club": "Real Sociedad", "club_league": "La Liga"},
        {"name": "Hakim Ziyech", "position": "W", "club": "Galatasaray", "club_league": "Super Lig"},
        {"name": "Youssef En-Nesyri", "position": "ST", "club": "Fenerbahce", "club_league": "Super Lig"},
        {"name": "Romain Saiss", "position": "CB", "club": "Al-Shabab", "club_league": "SPL"},
        {"name": "Noussair Mazraoui", "position": "FB", "club": "Manchester United", "club_league": "Premier League"},
        {"name": "Azzedine Ounahi", "position": "CM", "club": "Marseille", "club_league": "Ligue 1"},
        {"name": "Selim Amallah", "position": "AM", "club": "Valladolid", "club_league": "La Liga"},
        {"name": "Bilal El Khannouss", "position": "AM", "club": "Leicester", "club_league": "Premier League"},
        {"name": "Yahia Attiyat Allah", "position": "FB", "club": "Wydad", "club_league": "Botola Pro"},
        {"name": "Bounou", "position": "GK", "club": "Al-Hilal", "club_league": "SPL"},
        {"name": "Munir El Kajoui", "position": "GK", "club": "Al-Tai", "club_league": "SPL"},
        {"name": "Amine Harit", "position": "AM", "club": "Marseille", "club_league": "Ligue 1"},
        {"name": "Ez Abde", "position": "W", "club": "Betis", "club_league": "La Liga"},
        {"name": "Ismaila Sarr", "position": "W", "club": "Crystal Palace", "club_league": "Premier League"},
        {"name": "Walid Regragui", "position": "FB", "club": "Wydad", "club_league": "Botola Pro"},
        {"name": "Jawad El Yamiq", "position": "CB", "club": "Al-Wehda", "club_league": "SPL"},
        {"name": "Achraf Dari", "position": "CB", "club": "Al-Rayyan", "club_league": "Qatar Stars League"},
        {"name": "Zouhair El-Moutaraji", "position": "W", "club": "Wydad", "club_league": "Botola Pro"},
        {"name": "Soufiane Rahimi", "position": "W", "club": "Al-Ain", "club_league": "UAE Pro League"},
        {"name": "Oussama Idrissi", "position": "W", "club": "Cadiz", "club_league": "La Liga"},
        {"name": "Yahya Jabrane", "position": "CM", "club": "Wydad", "club_league": "Botola Pro"},
        {"name": "Adam Masina", "position": "FB", "club": "Udinese", "club_league": "Serie A"},
        {"name": "Samy Mmaee", "position": "CB", "club": "Ferencvaros", "club_league": "NB I"},
        {"name": "Aymen Barkok", "position": "AM", "club": "Mainz", "club_league": "Bundesliga"},
    ],
    "Netherlands": [
        {"name": "Bart Verbruggen", "position": "GK", "club": "Brighton", "club_league": "Premier League"},
        {"name": "Lutsharel Geertruida", "position": "FB", "club": "Sunderland", "club_league": "Premier League"},
        {"name": "Marten de Roon", "position": "CM", "club": "Atalanta", "club_league": "Serie A"},
        {"name": "Virgil van Dijk", "position": "CB", "club": "Liverpool", "club_league": "Premier League"},
        {"name": "Nathan Ake", "position": "CB", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Jan-Paul van Hecke", "position": "CB", "club": "Brighton", "club_league": "Premier League"},
        {"name": "Justin Kluivert", "position": "CM", "club": "Bournemouth", "club_league": "Premier League"},
        {"name": "Ryan Gravenberch", "position": "CM", "club": "Liverpool", "club_league": "Premier League"},
        {"name": "Wout Weghorst", "position": "ST", "club": "Ajax", "club_league": "Eredivisie"},
        {"name": "Memphis Depay", "position": "ST", "club": "Corinthians", "club_league": "Brasileirao"},
        {"name": "Cody Gakpo", "position": "W", "club": "Liverpool", "club_league": "Premier League"},
        {"name": "Mats Wieffer", "position": "CB", "club": "Brighton", "club_league": "Premier League"},
        {"name": "Robin Roefs", "position": "GK", "club": "Sunderland", "club_league": "Premier League"},
        {"name": "Tijjani Reijnders", "position": "CM", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Micky van de Ven", "position": "CB", "club": "Tottenham", "club_league": "Premier League"},
        {"name": "Guus Til", "position": "CM", "club": "PSV Eindhoven", "club_league": "Eredivisie"},
        {"name": "Noa Lang", "position": "W", "club": "Galatasaray", "club_league": "Super Lig"},
        {"name": "Donyell Malen", "position": "W", "club": "Roma", "club_league": "Serie A"},
        {"name": "Brian Brobbey", "position": "ST", "club": "Sunderland", "club_league": "Premier League"},
        {"name": "Teun Koopmeiners", "position": "CM", "club": "Juventus", "club_league": "Serie A"},
        {"name": "Frenkie de Jong", "position": "CM", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Denzel Dumfries", "position": "FB", "club": "Inter Milan", "club_league": "Serie A"},
        {"name": "Mark Flekken", "position": "GK", "club": "Bayer Leverkusen", "club_league": "Bundesliga"},
        {"name": "Crysencio Summerville", "position": "W", "club": "West Ham United", "club_league": "Premier League"},
        {"name": "Jorrel Hato", "position": "CB", "club": "Chelsea", "club_league": "Premier League"},
        {"name": "Quinten Timber", "position": "CM", "club": "Marseille", "club_league": "Ligue 1"},
    ],
    "New Zealand": [
        {"name": "Max Crocombe", "position": "GK", "club": "Millwall", "club_league": "EFL Championship"},
        {"name": "Tim Payne", "position": "FB", "club": "Wellington Phoenix", "club_league": "A-League"},
        {"name": "Francis de Vries", "position": "CB", "club": "Auckland FC", "club_league": "A-League"},
        {"name": "Tyler Bindon", "position": "CB", "club": "Sheffield United", "club_league": "Premier League"},
        {"name": "Michael Boxall", "position": "CB", "club": "Minnesota United", "club_league": "MLS"},
        {"name": "Joe Bell", "position": "CM", "club": "Viking", "club_league": "Eliteserien"},
        {"name": "Matthew Garbett", "position": "CM", "club": "Peterborough United", "club_league": "EFL Championship"},
        {"name": "Marko Stamenic", "position": "CM", "club": "Swansea City", "club_league": "EFL Championship"},
        {"name": "Chris Wood", "position": "ST", "club": "Nottingham Forest", "club_league": "Premier League"},
        {"name": "Sarpreet Singh", "position": "CM", "club": "Wellington Phoenix", "club_league": "A-League"},
        {"name": "Elijah Just", "position": "CM", "club": "Motherwell", "club_league": "Scottish Premiership"},
        {"name": "Alex Paulsen", "position": "GK", "club": "Lechia Gdansk", "club_league": "Ekstraklasa"},
        {"name": "Liberato Cacace", "position": "FB", "club": "Wrexham", "club_league": "EFL Championship"},
        {"name": "Alex Rufer", "position": "CM", "club": "Wellington Phoenix", "club_league": "A-League"},
        {"name": "Nando Pijnaker", "position": "CB", "club": "Auckland FC", "club_league": "A-League"},
        {"name": "Finn Surman", "position": "CB", "club": "Portland Timbers", "club_league": "MLS"},
        {"name": "Kosta Barbarouses", "position": "W", "club": "WS Wanderers", "club_league": "A-League"},
        {"name": "Ben Waine", "position": "ST", "club": "Port Vale", "club_league": "EFL Championship"},
        {"name": "Ben Old", "position": "CM", "club": "Saint-Etienne", "club_league": "Ligue 1"},
        {"name": "Callum McCowatt", "position": "CM", "club": "Silkeborg", "club_league": "Danish Superliga"},
        {"name": "Jesse Randall", "position": "ST", "club": "Auckland FC", "club_league": "A-League"},
        {"name": "Michael Woud", "position": "GK", "club": "Auckland FC", "club_league": "A-League"},
        {"name": "Ryan Thomas", "position": "CM", "club": "PEC Zwolle", "club_league": "Eredivisie"},
        {"name": "Callan Elliot", "position": "FB", "club": "Auckland FC", "club_league": "A-League"},
        {"name": "Lachlan Bayliss", "position": "CM", "club": "Newcastle Jets", "club_league": "A-League"},
        {"name": "Thomas Smith", "position": "CB", "club": "Braintree Town", "club_league": "National League"},
    ],
    "Norway": [
        {"name": "Orjan Nyland", "position": "GK", "club": "Sevilla", "club_league": "La Liga"},
        {"name": "Morten Thorsby", "position": "CM", "club": "Cremonese", "club_league": "Serie A"},
        {"name": "Kristoffer Ajer", "position": "CB", "club": "Brentford", "club_league": "Premier League"},
        {"name": "Leo Ostigard", "position": "CB", "club": "Genoa", "club_league": "Serie A"},
        {"name": "David Moller Wolfe", "position": "CB", "club": "Wolverhampton", "club_league": "Premier League"},
        {"name": "Patrick Berg", "position": "CM", "club": "Bodo/Glimt", "club_league": "Eliteserien"},
        {"name": "Alexander Sorloth", "position": "ST", "club": "Atletico Madrid", "club_league": "La Liga"},
        {"name": "Sander Berge", "position": "CM", "club": "Fulham", "club_league": "Premier League"},
        {"name": "Erling Haaland", "position": "ST", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Martin Odegaard", "position": "AM", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Jorgen Strand Larsen", "position": "ST", "club": "Crystal Palace", "club_league": "Premier League"},
        {"name": "Sander Tangvik", "position": "GK", "club": "Hamburger SV", "club_league": "2. Bundesliga"},
        {"name": "Egil Selvik", "position": "GK", "club": "Watford", "club_league": "EFL Championship"},
        {"name": "Fredrik Aursnes", "position": "CM", "club": "Benfica", "club_league": "Liga Portugal"},
        {"name": "Fredrik Bjorkan", "position": "FB", "club": "Bodo/Glimt", "club_league": "Eliteserien"},
        {"name": "Marcus Holmgren Pedersen", "position": "FB", "club": "Torino", "club_league": "Serie A"},
        {"name": "Torbjorn Heggem", "position": "CB", "club": "Bologna", "club_league": "Serie A"},
        {"name": "Kristian Thorstvedt", "position": "CM", "club": "Sassuolo", "club_league": "Serie A"},
        {"name": "Thelonious Aasgaard", "position": "CM", "club": "Rangers", "club_league": "Scottish Premiership"},
        {"name": "Antonio Nusa", "position": "W", "club": "RB Leipzig", "club_league": "Bundesliga"},
        {"name": "Andreas Schjelderup", "position": "CM", "club": "Benfica", "club_league": "Liga Portugal"},
        {"name": "Oscar Bobb", "position": "CM", "club": "Fulham", "club_league": "Premier League"},
        {"name": "Jens Petter Hauge", "position": "CM", "club": "Bodo/Glimt", "club_league": "Eliteserien"},
        {"name": "Sondre Langas", "position": "CB", "club": "Derby County", "club_league": "EFL Championship"},
        {"name": "Henrik Falchener", "position": "CB", "club": "Viking", "club_league": "Eliteserien"},
        {"name": "Julian Ryerson", "position": "W", "club": "Dortmund", "club_league": "Bundesliga"},
    ],
    "Panama": [
        {"name": "Luis Mejia", "position": "GK", "club": "Club Nacional", "club_league": "Uruguayan Primera"},
        {"name": "Cesar Blackman", "position": "FB", "club": "Slovan Bratislava", "club_league": "Slovak Super Liga"},
        {"name": "Jose Cordoba", "position": "CB", "club": "Norwich City", "club_league": "EFL Championship"},
        {"name": "Fidel Escobar", "position": "CB", "club": "Deportivo Saprissa", "club_league": "Liga FPD"},
        {"name": "Edgardo Farina", "position": "CB", "club": "Pari NN", "club_league": "RFPL"},
        {"name": "Cristian Martinez", "position": "CM", "club": "Hapoel Kiryat Shmona", "club_league": "Israeli Premier League"},
        {"name": "Jose Luis Rodriguez", "position": "CM", "club": "FC Juarez", "club_league": "Liga MX"},
        {"name": "Adalberto Carrasquilla", "position": "CM", "club": "Pumas UNAM", "club_league": "Liga MX"},
        {"name": "Tomas Rodriguez", "position": "ST", "club": "Deportivo Saprissa", "club_league": "Liga FPD"},
        {"name": "Ismael Diaz", "position": "CM", "club": "Club Leon", "club_league": "Liga MX"},
        {"name": "Edgar Barcenas", "position": "CM", "club": "Mazatlan", "club_league": "Liga MX"},
        {"name": "Cesar Samudio", "position": "GK", "club": "CD Marathon", "club_league": "Liga Nacional"},
        {"name": "Jiovany Ramos", "position": "CB", "club": "Puerto Cabello", "club_league": "Venezuelan Primera"},
        {"name": "Carlos Harvey", "position": "CB", "club": "Minnesota United", "club_league": "MLS"},
        {"name": "Eric Davis", "position": "FB", "club": "CD Plaza Amador", "club_league": "LPF"},
        {"name": "Andres Andrade", "position": "CB", "club": "LASK Linz", "club_league": "Austrian Bundesliga"},
        {"name": "Jose Fajardo", "position": "ST", "club": "Universidad Catolica", "club_league": "Ecuadorian Serie A"},
        {"name": "Cecilio Waterman", "position": "ST", "club": "Universidad de Concepcion", "club_league": "Chilean Primera"},
        {"name": "Alberto Quintero", "position": "CM", "club": "CD Plaza Amador", "club_league": "LPF"},
        {"name": "Anibal Godoy", "position": "CM", "club": "San Diego FC", "club_league": "MLS"},
        {"name": "Cesar Yanis", "position": "CM", "club": "CD Cobresal", "club_league": "Chilean Primera"},
        {"name": "Orlando Mosquera", "position": "GK", "club": "Al Fayha", "club_league": "SPL"},
        {"name": "Michael Murillo", "position": "FB", "club": "Besiktas", "club_league": "Super Lig"},
        {"name": "Azarias Londoño", "position": "ST", "club": "Universidad Catolica", "club_league": "Ecuadorian Serie A"},
        {"name": "Roderick Miller", "position": "CB", "club": "Turan Tovuz", "club_league": "Azerbaijan Premier League"},
        {"name": "Jorge Gutierrez", "position": "CB", "club": "Deportivo La Guaira", "club_league": "Venezuelan Primera"},
    ],
    "Paraguay": [
        {"name": "Roberto Fernandez", "position": "GK", "club": "Cerro Porteno", "club_league": "Paraguayan Primera"},
        {"name": "Victor Velazquez", "position": "CB", "club": "Cerro Porteno", "club_league": "Paraguayan Primera"},
        {"name": "Omar Alderete", "position": "CB", "club": "Sunderland", "club_league": "Premier League"},
        {"name": "Juan Jose Caceres", "position": "CB", "club": "Dynamo Moscow", "club_league": "RFPL"},
        {"name": "Fabian Balbuena", "position": "CB", "club": "Gremio", "club_league": "Brasileirao"},
        {"name": "Junior Alonso", "position": "CB", "club": "Atletico Mineiro", "club_league": "Brasileirao"},
        {"name": "Ramon Sosa", "position": "CM", "club": "Palmeiras", "club_league": "Brasileirao"},
        {"name": "Diego Gomez", "position": "CM", "club": "Brighton", "club_league": "Premier League"},
        {"name": "Antonio Sanabria", "position": "ST", "club": "Cremonese", "club_league": "Serie A"},
        {"name": "Miguel Almiron", "position": "CM", "club": "Atlanta United", "club_league": "MLS"},
        {"name": "Mauricio Prado", "position": "CM", "club": "Palmeiras", "club_league": "Brasileirao"},
        {"name": "Orlando Gill", "position": "GK", "club": "San Lorenzo", "club_league": "Liga Profesional"},
        {"name": "Jose Maria Canale", "position": "CB", "club": "Lanus", "club_league": "Liga Profesional"},
        {"name": "Adrian Cubas", "position": "CM", "club": "Vancouver Whitecaps", "club_league": "MLS"},
        {"name": "Gustavo Gomez", "position": "CB", "club": "Palmeiras", "club_league": "Brasileirao"},
        {"name": "Damian Bobadilla", "position": "CM", "club": "Sao Paulo", "club_league": "Brasileirao"},
        {"name": "Alejandro Romero Gamarra", "position": "ST", "club": "Al Ain", "club_league": "UAE Pro League"},
        {"name": "Alex Arce", "position": "ST", "club": "Independiente Rivadavia", "club_league": "Liga Profesional"},
        {"name": "Julio Enciso", "position": "ST", "club": "Strasbourg", "club_league": "Ligue 1"},
        {"name": "Braian Ojeda", "position": "CM", "club": "Orlando City", "club_league": "MLS"},
        {"name": "Gabriel Avalos", "position": "ST", "club": "Independiente", "club_league": "Liga Profesional"},
        {"name": "Gaston Olveira", "position": "GK", "club": "Club Olimpia", "club_league": "Paraguayan Primera"},
        {"name": "Matias Galarza", "position": "CM", "club": "Atlanta United", "club_league": "MLS"},
        {"name": "Gustavo Caballero", "position": "CM", "club": "Portsmouth", "club_league": "EFL Championship"},
        {"name": "Isidro Pitta", "position": "ST", "club": "Red Bull Bragantino", "club_league": "Brasileirao"},
        {"name": "Alexandro Maidana", "position": "CB", "club": "Talleres", "club_league": "Liga Profesional"},
    ],
    "Portugal": [
        {"name": "Diogo Costa", "position": "GK", "club": "Porto", "club_league": "Liga Portugal"},
        {"name": "Nelson Semedo", "position": "FB", "club": "Fenerbahce", "club_league": "Super Lig"},
        {"name": "Ruben Dias", "position": "CB", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Tomas Araujo", "position": "CB", "club": "Benfica", "club_league": "Liga Portugal"},
        {"name": "Diogo Dalot", "position": "FB", "club": "Manchester United", "club_league": "Premier League"},
        {"name": "Matheus Nunes", "position": "CM", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Cristiano Ronaldo", "position": "ST", "club": "Al-Nassr", "club_league": "SPL"},
        {"name": "Bruno Fernandes", "position": "AM", "club": "Manchester United", "club_league": "Premier League"},
        {"name": "Goncalo Ramos", "position": "ST", "club": "PSG", "club_league": "Ligue 1"},
        {"name": "Bernardo Silva", "position": "CM", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Joao Felix", "position": "ST", "club": "Al-Nassr", "club_league": "SPL"},
        {"name": "Jose Sa", "position": "GK", "club": "Wolverhampton", "club_league": "Premier League"},
        {"name": "Renato Veiga", "position": "CB", "club": "Villarreal", "club_league": "La Liga"},
        {"name": "Goncalo Inacio", "position": "CB", "club": "Sporting CP", "club_league": "Liga Portugal"},
        {"name": "Joao Neves", "position": "CM", "club": "PSG", "club_league": "Ligue 1"},
        {"name": "Trincao", "position": "W", "club": "Sporting CP", "club_league": "Liga Portugal"},
        {"name": "Rafael Leao", "position": "W", "club": "AC Milan", "club_league": "Serie A"},
        {"name": "Pedro Neto", "position": "W", "club": "Chelsea", "club_league": "Premier League"},
        {"name": "Goncalo Guedes", "position": "W", "club": "Real Sociedad", "club_league": "La Liga"},
        {"name": "Joao Cancelo", "position": "FB", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Ruben Neves", "position": "CM", "club": "Al-Hilal", "club_league": "SPL"},
        {"name": "Rui Silva", "position": "GK", "club": "Sporting CP", "club_league": "Liga Portugal"},
        {"name": "Vitinha", "position": "CM", "club": "PSG", "club_league": "Ligue 1"},
        {"name": "Samu Costa", "position": "CB", "club": "Mallorca", "club_league": "La Liga"},
        {"name": "Nuno Mendes", "position": "FB", "club": "PSG", "club_league": "Ligue 1"},
        {"name": "Francisco Conceicao", "position": "W", "club": "Juventus", "club_league": "Serie A"},
    ],
    "Qatar": [
        {"name": "Mahmoud Abunada", "position": "GK", "club": "Al-Rayyan", "club_league": "Qatar Stars League"},
        {"name": "Pedro Miguel", "position": "FB", "club": "Al-Sadd", "club_league": "Qatar Stars League"},
        {"name": "Lucas Mendes", "position": "CB", "club": "Al-Wakrah", "club_league": "Qatar Stars League"},
        {"name": "Gueye", "position": "CB", "club": "Al-Lusail", "club_league": "Qatar Stars League"},
        {"name": "Jassem Gaber", "position": "CB", "club": "Al-Duhail", "club_league": "Qatar Stars League"},
        {"name": "Abdelaziz Hatim", "position": "CM", "club": "Al-Rayyan", "club_league": "Qatar Stars League"},
        {"name": "Ahmed Alaaeldin", "position": "ST", "club": "Al-Rayyan", "club_league": "Qatar Stars League"},
        {"name": "Edmilson Junior", "position": "ST", "club": "Al-Duhail", "club_league": "Qatar Stars League"},
        {"name": "Mohammed Muntari", "position": "ST", "club": "Al-Gharafa", "club_league": "Qatar Stars League"},
        {"name": "Hasan Alhaydos", "position": "ST", "club": "Al-Sadd", "club_league": "Qatar Stars League"},
        {"name": "Akram Afif", "position": "W", "club": "Al-Sadd", "club_league": "Qatar Stars League"},
        {"name": "Karim Boudiaf", "position": "CM", "club": "Al-Duhail", "club_league": "Qatar Stars League"},
        {"name": "Ayoub Aloui", "position": "CB", "club": "Al-Gharafa", "club_league": "Qatar Stars League"},
        {"name": "Homam Ahmed", "position": "CB", "club": "Cultural Leonesa", "club_league": "Segunda Division"},
        {"name": "Yusuf Abdurisag", "position": "ST", "club": "Al-Wakrah", "club_league": "Qatar Stars League"},
        {"name": "Boualem Khoukhi", "position": "CB", "club": "Al-Sadd", "club_league": "Qatar Stars League"},
        {"name": "Ahmed AlGanehi", "position": "CM", "club": "Al-Arabi SC", "club_league": "Qatar Stars League"},
        {"name": "Sultan Al-Brake", "position": "CB", "club": "Al-Duhail", "club_league": "Qatar Stars League"},
        {"name": "Almoez Ali", "position": "ST", "club": "Al-Duhail", "club_league": "Qatar Stars League"},
        {"name": "Ahmed Fathy", "position": "CM", "club": "Al-Arabi SC", "club_league": "Qatar Stars League"},
        {"name": "Salah Zakaria", "position": "GK", "club": "Al-Duhail", "club_league": "Qatar Stars League"},
        {"name": "Meshaal Barsham", "position": "GK", "club": "Al-Sadd", "club_league": "Qatar Stars League"},
        {"name": "Assim Madibo", "position": "CM", "club": "Al-Wakrah", "club_league": "Qatar Stars League"},
        {"name": "Tahsin Jamshid", "position": "ST", "club": "Al-Duhail", "club_league": "Qatar Stars League"},
        {"name": "Alhashmi Mohialdin", "position": "CB", "club": "Al-Arabi SC", "club_league": "Qatar Stars League"},
        {"name": "Mohamed Manai", "position": "ST", "club": "Al-Khor", "club_league": "Qatar Stars League"},
    ],
    "Saudi Arabia": [
        {"name": "Nawaf Al-Aqidi", "position": "GK", "club": "Al-Nassr", "club_league": "SPL"},
        {"name": "Ali Majrashi", "position": "FB", "club": "Al-Ahli", "club_league": "SPL"},
        {"name": "Ali Lajami", "position": "CB", "club": "Al-Hilal", "club_league": "SPL"},
        {"name": "Abdulelah Al-Amri", "position": "CB", "club": "Al-Nassr", "club_league": "SPL"},
        {"name": "Hassan Al-Tambakti", "position": "CB", "club": "Al-Hilal", "club_league": "SPL"},
        {"name": "Nasser Al-Dawsari", "position": "CM", "club": "Al-Hilal", "club_league": "SPL"},
        {"name": "Musab Al-Juwayr", "position": "CM", "club": "Al-Qadsiah", "club_league": "SPL"},
        {"name": "Aiman Ahmed", "position": "W", "club": "Al-Nassr", "club_league": "SPL"},
        {"name": "Firas Al-Brikan", "position": "ST", "club": "Al-Ahli", "club_league": "SPL"},
        {"name": "Salem Al-Dawsari", "position": "W", "club": "Al-Hilal", "club_league": "SPL"},
        {"name": "Saleh Al-Shehri", "position": "ST", "club": "Al-Ittihad", "club_league": "SPL"},
        {"name": "Saud Abdulhamid", "position": "FB", "club": "Lens", "club_league": "Ligue 1"},
        {"name": "Nawaf Bu Washl", "position": "CB", "club": "Al-Nassr", "club_league": "SPL"},
        {"name": "Hassan Kadish", "position": "CB", "club": "Al-Ittihad", "club_league": "SPL"},
        {"name": "Abdullah Al-Khaibari", "position": "CM", "club": "Al-Nassr", "club_league": "SPL"},
        {"name": "Ziyad Al-Johani", "position": "CM", "club": "Al-Ahli", "club_league": "SPL"},
        {"name": "Khalid Al-Ghannam", "position": "W", "club": "Al-Nassr", "club_league": "SPL"},
        {"name": "Ala Al-Hajji", "position": "CM", "club": "Neom SC", "club_league": "SPL"},
        {"name": "Abdullah Al-Hamddan", "position": "ST", "club": "Al-Nassr", "club_league": "SPL"},
        {"name": "Sultan Mandash", "position": "W", "club": "Al-Hilal", "club_league": "SPL"},
        {"name": "Mohammed Al-Owais", "position": "GK", "club": "Al-Hilal", "club_league": "SPL"},
        {"name": "Ahmed Al-Kassar", "position": "GK", "club": "Al-Qadsiah", "club_league": "SPL"},
        {"name": "Mohamed Kanno", "position": "CM", "club": "Al-Hilal", "club_league": "SPL"},
        {"name": "Moteb Al-Harbi", "position": "FB", "club": "Al-Hilal", "club_league": "SPL"},
        {"name": "Jehad Thikri", "position": "CB", "club": "Al-Qadsiah", "club_league": "SPL"},
        {"name": "Mohammed Abu Alshamat", "position": "CM", "club": "Al-Ahli", "club_league": "SPL"},
    ],
    "Scotland": [
        {"name": "Angus Gunn", "position": "GK", "club": "Nottingham Forest", "club_league": "Premier League"},
        {"name": "Aaron Hickey", "position": "FB", "club": "Brentford", "club_league": "Premier League"},
        {"name": "Andrew Robertson", "position": "FB", "club": "Liverpool", "club_league": "Premier League"},
        {"name": "Scott McTominay", "position": "CM", "club": "Napoli", "club_league": "Serie A"},
        {"name": "Grant Hanley", "position": "CB", "club": "Hibernian", "club_league": "Scottish Premiership"},
        {"name": "Kieran Tierney", "position": "FB", "club": "Celtic", "club_league": "Scottish Premiership"},
        {"name": "John McGinn", "position": "CM", "club": "Aston Villa", "club_league": "Premier League"},
        {"name": "Tyler Fletcher", "position": "CM", "club": "Manchester United", "club_league": "Premier League"},
        {"name": "Lyndon Dykes", "position": "ST", "club": "Charlton Athletic", "club_league": "EFL Championship"},
        {"name": "Che Adams", "position": "ST", "club": "Torino", "club_league": "Serie A"},
        {"name": "Ryan Christie", "position": "CM", "club": "Bournemouth", "club_league": "Premier League"},
        {"name": "Liam Kelly", "position": "GK", "club": "Rangers", "club_league": "Scottish Premiership"},
        {"name": "Jack Hendry", "position": "CB", "club": "Al-Ettifaq", "club_league": "SPL"},
        {"name": "Ross Stewart", "position": "ST", "club": "Southampton", "club_league": "EFL Championship"},
        {"name": "John Souttar", "position": "CB", "club": "Rangers", "club_league": "Scottish Premiership"},
        {"name": "Dominic Hyam", "position": "CB", "club": "Wrexham", "club_league": "EFL Championship"},
        {"name": "Ben Doak", "position": "W", "club": "Bournemouth", "club_league": "Premier League"},
        {"name": "George Hirst", "position": "ST", "club": "Ipswich", "club_league": "Premier League"},
        {"name": "Lewis Ferguson", "position": "CM", "club": "Bologna", "club_league": "Serie A"},
        {"name": "Lawrence Shankland", "position": "ST", "club": "Hearts", "club_league": "Scottish Premiership"},
        {"name": "Craig Gordon", "position": "GK", "club": "Hearts", "club_league": "Scottish Premiership"},
        {"name": "Nathan Patterson", "position": "FB", "club": "Everton", "club_league": "Premier League"},
        {"name": "Kenny McLean", "position": "CM", "club": "Norwich", "club_league": "EFL Championship"},
        {"name": "Anthony Ralston", "position": "FB", "club": "Celtic", "club_league": "Scottish Premiership"},
        {"name": "Findlay Curtis", "position": "W", "club": "Kilmarnock", "club_league": "Scottish Premiership"},
        {"name": "Scott McKenna", "position": "CB", "club": "Dinamo Zagreb", "club_league": "HNL"},
    ],
    "Senegal": [
        {"name": "Yehvann Diop", "position": "GK", "club": "Nice", "club_league": "Ligue 1"},
        {"name": "Mamadou Sarr", "position": "CB", "club": "Chelsea", "club_league": "Premier League"},
        {"name": "Kalidou Koulibaly", "position": "CB", "club": "Al-Hilal", "club_league": "SPL"},
        {"name": "Abdoulaye Seck", "position": "CB", "club": "Maccabi Haifa", "club_league": "Ligat HaAl"},
        {"name": "Idrissa Gueye", "position": "DM", "club": "Everton", "club_league": "Premier League"},
        {"name": "Pate Siss", "position": "CM", "club": "Rayo Vallecano", "club_league": "La Liga"},
        {"name": "Assane Diao", "position": "W", "club": "Como", "club_league": "Serie A"},
        {"name": "Lamine Camara", "position": "CM", "club": "Monaco", "club_league": "Ligue 1"},
        {"name": "Bamba Dieng", "position": "ST", "club": "Lorient", "club_league": "Ligue 1"},
        {"name": "Sadio Mane", "position": "W", "club": "Al-Nassr", "club_league": "SPL"},
        {"name": "Nicolas Jackson", "position": "ST", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Pape Cherif Ndiaye", "position": "ST", "club": "Samsunspor", "club_league": "Super Lig"},
        {"name": "Iliman Ndiaye", "position": "AM", "club": "Everton", "club_league": "Premier League"},
        {"name": "Ismail Jacobs", "position": "FB", "club": "Galatasaray", "club_league": "Super Lig"},
        {"name": "Krepin Diatta", "position": "FB", "club": "Monaco", "club_league": "Ligue 1"},
        {"name": "Edouard Mendy", "position": "GK", "club": "Al-Ahli", "club_league": "SPL"},
        {"name": "Pape Matar Sarr", "position": "CM", "club": "Tottenham", "club_league": "Premier League"},
        {"name": "Ismaila Sarr", "position": "W", "club": "Crystal Palace", "club_league": "Premier League"},
        {"name": "Moussa Niakhate", "position": "CB", "club": "Lyon", "club_league": "Ligue 1"},
        {"name": "Ibrahim Mbaye", "position": "W", "club": "PSG", "club_league": "Ligue 1"},
        {"name": "Habib Diarra", "position": "CM", "club": "Sunderland", "club_league": "EFL Championship"},
        {"name": "Bara Sapoco Ndiaye", "position": "CM", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Mory Diop", "position": "GK", "club": "Le Havre", "club_league": "Ligue 1"},
        {"name": "Antoine Mendy", "position": "FB", "club": "Nice", "club_league": "Ligue 1"},
        {"name": "El Hadji Malick Diouf", "position": "FB", "club": "West Ham", "club_league": "Premier League"},
        {"name": "Pape Alassane Gueye", "position": "CM", "club": "Villarreal", "club_league": "La Liga"},
    ],
    "South Africa": [
        {"name": "Ronwen Williams", "position": "GK", "club": "Mamelodi Sundowns", "club_league": "PSL"},
        {"name": "Tholo Matuludi", "position": "FB", "club": "Polokwane City", "club_league": "PSL"},
        {"name": "Khulumani Ndamane", "position": "CB", "club": "Mamelodi Sundowns", "club_league": "PSL"},
        {"name": "Teboho Mokoena", "position": "CM", "club": "Mamelodi Sundowns", "club_league": "PSL"},
        {"name": "Thalente Mbatha", "position": "CM", "club": "Orlando Pirates", "club_league": "PSL"},
        {"name": "Aubrey Modiba", "position": "FB", "club": "Mamelodi Sundowns", "club_league": "PSL"},
        {"name": "Oswin Appollis", "position": "W", "club": "Orlando Pirates", "club_league": "PSL"},
        {"name": "Tshepang Moremi", "position": "W", "club": "Orlando Pirates", "club_league": "PSL"},
        {"name": "Lyle Foster", "position": "ST", "club": "Burnley", "club_league": "Premier League"},
        {"name": "Relebohile Mofokeng", "position": "W", "club": "Orlando Pirates", "club_league": "PSL"},
        {"name": "Themba Zwane", "position": "CM", "club": "Mamelodi Sundowns", "club_league": "PSL"},
        {"name": "Thapelo Maseko", "position": "W", "club": "AEL Limassol", "club_league": "Cypriot First Division"},
        {"name": "Sphephelo Sithole", "position": "CM", "club": "Tondela", "club_league": "Liga Portugal"},
        {"name": "Mbekezeli Mbokazi", "position": "CB", "club": "Chicago Fire", "club_league": "MLS"},
        {"name": "Iqraam Rayners", "position": "ST", "club": "Mamelodi Sundowns", "club_league": "PSL"},
        {"name": "Sipho Chaine", "position": "GK", "club": "Orlando Pirates", "club_league": "PSL"},
        {"name": "Evidence Makgopa", "position": "ST", "club": "Orlando Pirates", "club_league": "PSL"},
        {"name": "Samukele Kabini", "position": "CB", "club": "Molde", "club_league": "Eliteserien"},
        {"name": "Nkosinathi Sibisi", "position": "CB", "club": "Orlando Pirates", "club_league": "PSL"},
        {"name": "Khuliso Mudau", "position": "FB", "club": "Mamelodi Sundowns", "club_league": "PSL"},
        {"name": "Ime Okon", "position": "CB", "club": "Hannover 96", "club_league": "Bundesliga"},
        {"name": "Stuart Goss", "position": "GK", "club": "Siwelele", "club_league": "PSL"},
        {"name": "Jayden Adams", "position": "CM", "club": "Mamelodi Sundowns", "club_league": "PSL"},
        {"name": "Olwethu Makhanya", "position": "CB", "club": "Philadelphia Union", "club_league": "MLS"},
        {"name": "Kamogelo Sebebelebe", "position": "W", "club": "Orlando Pirates", "club_league": "PSL"},
        {"name": "Bradley Cross", "position": "CB", "club": "Kaizer Chiefs", "club_league": "PSL"},
    ],
    "South Korea": [
        {"name": "Kim Seunggyu", "position": "GK", "club": "FC Tokyo", "club_league": "J-League"},
        {"name": "Lee Hanbeom", "position": "CB", "club": "Midtjylland", "club_league": "Danish Superliga"},
        {"name": "Lee Gihyuk", "position": "CM", "club": "Gangwon FC", "club_league": "K League 1"},
        {"name": "Kim Minjae", "position": "CB", "club": "Bayern Munich", "club_league": "Bundesliga"},
        {"name": "Kim Taehyeon", "position": "CB", "club": "Kashima Antlers", "club_league": "J-League"},
        {"name": "Hwang Inbeom", "position": "CM", "club": "Feyenoord", "club_league": "Eredivisie"},
        {"name": "Son Heung Min", "position": "W", "club": "LAFC", "club_league": "MLS"},
        {"name": "Paik Seungho", "position": "CM", "club": "Birmingham City", "club_league": "EFL Championship"},
        {"name": "Cho Guesung", "position": "ST", "club": "Midtjylland", "club_league": "Danish Superliga"},
        {"name": "Lee Jae Sung", "position": "CM", "club": "Mainz 05", "club_league": "Bundesliga"},
        {"name": "Hwang Hee Chan", "position": "W", "club": "Wolverhampton", "club_league": "Premier League"},
        {"name": "Song Bumkeun", "position": "GK", "club": "Jeonbuk Hyundai Motors", "club_league": "K League 1"},
        {"name": "Lee Taeseok", "position": "CB", "club": "Austria Wien", "club_league": "Austrian Bundesliga"},
        {"name": "Cho Wije", "position": "CB", "club": "Sharjah", "club_league": "UAE Pro League"},
        {"name": "Kim Moonhwan", "position": "FB", "club": "Daejeon Hana Citizen", "club_league": "K League 1"},
        {"name": "Park Jinseob", "position": "CB", "club": "Zhejiang Professional", "club_league": "Chinese Super League"},
        {"name": "Bae Junho", "position": "CM", "club": "Celtic", "club_league": "Scottish Premiership"},
        {"name": "Oh Hyeongyu", "position": "ST", "club": "Besiktas", "club_league": "Super Lig"},
        {"name": "Lee Kangin", "position": "AM", "club": "PSG", "club_league": "Ligue 1"},
        {"name": "Yang Hyunjun", "position": "CM", "club": "Swansea City", "club_league": "EFL Championship"},
        {"name": "Jo Hyeonwoo", "position": "GK", "club": "Ulsan HD", "club_league": "K League 1"},
        {"name": "Seol Youngwoo", "position": "FB", "club": "Red Star Belgrade", "club_league": "Serbian SuperLiga"},
        {"name": "Jens Castrop", "position": "FB", "club": "Borussia Monchengladbach", "club_league": "Bundesliga"},
        {"name": "Kim Jingyu", "position": "CM", "club": "Jeonbuk Hyundai Motors", "club_league": "K League 1"},
        {"name": "Eom Jisung", "position": "CM", "club": "Stoke City", "club_league": "EFL Championship"},
        {"name": "Lee Donggyeong", "position": "CM", "club": "Ulsan HD", "club_league": "K League 1"},
    ],
    "Spain": [
        {"name": "David Raya", "position": "GK", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Marc Pubill", "position": "FB", "club": "Atletico Madrid", "club_league": "La Liga"},
        {"name": "Alejandro Grimaldo", "position": "FB", "club": "Bayer Leverkusen", "club_league": "Bundesliga"},
        {"name": "Eric Garcia", "position": "CB", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Marcos Llorente", "position": "FB", "club": "Atletico Madrid", "club_league": "La Liga"},
        {"name": "Mikel Merino", "position": "CM", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Ferran Torres", "position": "W", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Fabian Ruiz", "position": "CM", "club": "PSG", "club_league": "Ligue 1"},
        {"name": "Gavi", "position": "AM", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Dani Olmo", "position": "AM", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Yeremy Pino", "position": "W", "club": "Crystal Palace", "club_league": "Premier League"},
        {"name": "Pedro Porro", "position": "FB", "club": "Tottenham", "club_league": "Premier League"},
        {"name": "Joan Garcia", "position": "GK", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Aymeric Laporte", "position": "CB", "club": "Athletic Bilbao", "club_league": "La Liga"},
        {"name": "Alex Baena", "position": "CM", "club": "Atletico Madrid", "club_league": "La Liga"},
        {"name": "Rodri", "position": "DM", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Nico Williams", "position": "W", "club": "Athletic Bilbao", "club_league": "La Liga"},
        {"name": "Martin Zubimendi", "position": "DM", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Lamine Yamal", "position": "W", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Pedri", "position": "CM", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Mikel Oyarzabal", "position": "ST", "club": "Real Sociedad", "club_league": "La Liga"},
        {"name": "Pau Cubarsi", "position": "CB", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Unai Simon", "position": "GK", "club": "Athletic Bilbao", "club_league": "La Liga"},
        {"name": "Marc Cucurella", "position": "FB", "club": "Chelsea", "club_league": "Premier League"},
        {"name": "Victor Munoz", "position": "W", "club": "Osasuna", "club_league": "La Liga"},
        {"name": "Borja Iglesias", "position": "ST", "club": "Celta Vigo", "club_league": "La Liga"},
    ],
    "Sweden": [
        {"name": "Jacob Widell Zetterstrom", "position": "GK", "club": "Derby County", "club_league": "EFL Championship"},
        {"name": "Gustaf Lagerbielke", "position": "CB", "club": "Braga", "club_league": "Liga Portugal"},
        {"name": "Victor Lindelof", "position": "CB", "club": "Aston Villa", "club_league": "Premier League"},
        {"name": "Isak Hien", "position": "CB", "club": "Atalanta", "club_league": "Serie A"},
        {"name": "Gabriel Gudmundsson", "position": "FB", "club": "Leeds", "club_league": "Premier League"},
        {"name": "Herman Johansson", "position": "CB", "club": "FC Dallas", "club_league": "MLS"},
        {"name": "Lucas Bergvall", "position": "CM", "club": "Tottenham", "club_league": "Premier League"},
        {"name": "Daniel Svensson", "position": "FB", "club": "Dortmund", "club_league": "Bundesliga"},
        {"name": "Alexander Isak", "position": "ST", "club": "Liverpool", "club_league": "Premier League"},
        {"name": "Benjamin Nygren", "position": "CM", "club": "Celtic", "club_league": "Scottish Premiership"},
        {"name": "Anthony Elanga", "position": "W", "club": "Newcastle", "club_league": "Premier League"},
        {"name": "Tobias Johansson", "position": "GK", "club": "Stoke City", "club_league": "EFL Championship"},
        {"name": "Ken Sema", "position": "CM", "club": "Pafos", "club_league": "Cypriot First Division"},
        {"name": "Hjalmar Ekdal", "position": "CB", "club": "Burnley", "club_league": "Premier League"},
        {"name": "Carl Starfelt", "position": "CB", "club": "Celta Vigo", "club_league": "La Liga"},
        {"name": "Jesper Karlstrom", "position": "CM", "club": "Udinese", "club_league": "Serie A"},
        {"name": "Viktor Gyokeres", "position": "ST", "club": "Arsenal", "club_league": "Premier League"},
        {"name": "Yasin Ayari", "position": "CM", "club": "Brighton", "club_league": "Premier League"},
        {"name": "Mattias Svanberg", "position": "CM", "club": "Wolfsburg", "club_league": "Bundesliga"},
        {"name": "Eric Smith", "position": "FB", "club": "St. Pauli", "club_league": "Bundesliga"},
        {"name": "Alexander Bernhardsson", "position": "FB", "club": "Holstein Kiel", "club_league": "Bundesliga"},
        {"name": "Besfort Zeneli", "position": "CM", "club": "Union SG", "club_league": "Jupiler Pro League"},
        {"name": "Kristoffer Nordfeldt", "position": "GK", "club": "AIK", "club_league": "Allsvenskan"},
        {"name": "Elliot Stroud", "position": "CB", "club": "Mjallby", "club_league": "Allsvenskan"},
        {"name": "Hakan Nilsson", "position": "ST", "club": "Club Brugge", "club_league": "Jupiler Pro League"},
        {"name": "Taha Ali", "position": "W", "club": "Malmo", "club_league": "Allsvenskan"},
    ],
    "Switzerland": [
        {"name": "Gregor Kobel", "position": "GK", "club": "Dortmund", "club_league": "Bundesliga"},
        {"name": "Miro Muheim", "position": "FB", "club": "Hamburger SV", "club_league": "Bundesliga"},
        {"name": "Silvan Widmer", "position": "FB", "club": "Mainz", "club_league": "Bundesliga"},
        {"name": "Nico Elvedi", "position": "CB", "club": "M'gladbach", "club_league": "Bundesliga"},
        {"name": "Manuel Akanji", "position": "CB", "club": "Inter Milan", "club_league": "Serie A"},
        {"name": "Denis Zakaria", "position": "CM", "club": "Monaco", "club_league": "Ligue 1"},
        {"name": "Breel Embolo", "position": "ST", "club": "Rennes", "club_league": "Ligue 1"},
        {"name": "Remo Freuler", "position": "CM", "club": "Bologna", "club_league": "Serie A"},
        {"name": "Johan Manzambi", "position": "CM", "club": "Freiburg", "club_league": "Bundesliga"},
        {"name": "Granit Xhaka", "position": "CM", "club": "Sunderland", "club_league": "EFL Championship"},
        {"name": "Dan Ndoye", "position": "W", "club": "Nottingham Forest", "club_league": "Premier League"},
        {"name": "Yvon Mvogo", "position": "GK", "club": "Lorient", "club_league": "Ligue 1"},
        {"name": "Ricardo Rodriguez", "position": "CB", "club": "Real Betis", "club_league": "La Liga"},
        {"name": "Ardon Jashari", "position": "CM", "club": "AC Milan", "club_league": "Serie A"},
        {"name": "Djibril Sow", "position": "CM", "club": "Sevilla", "club_league": "La Liga"},
        {"name": "Christian Fassnacht", "position": "W", "club": "Young Boys", "club_league": "Swiss Super League"},
        {"name": "Ruben Vargas", "position": "W", "club": "Sevilla", "club_league": "La Liga"},
        {"name": "Eray Comert", "position": "CB", "club": "Valencia", "club_league": "La Liga"},
        {"name": "Noah Okafor", "position": "W", "club": "Leeds", "club_league": "Premier League"},
        {"name": "Michel Aebischer", "position": "CM", "club": "Pisa", "club_league": "Serie A"},
        {"name": "Marvin Keller", "position": "GK", "club": "Young Boys", "club_league": "Swiss Super League"},
        {"name": "Fabian Rieder", "position": "CM", "club": "Augsburg", "club_league": "Bundesliga"},
        {"name": "Zeki Amdouni", "position": "ST", "club": "Burnley", "club_league": "Premier League"},
        {"name": "Aurele Amenda", "position": "CB", "club": "Ein Frankfurt", "club_league": "Bundesliga"},
        {"name": "Luca Jaquez", "position": "CB", "club": "Stuttgart", "club_league": "Bundesliga"},
        {"name": "Cedric Itten", "position": "ST", "club": "Fortuna Dusseldorf", "club_league": "Bundesliga"},
    ],
    "Tunisia": [
        {"name": "Abdelmouhib Chamakh", "position": "GK", "club": "Club Africain", "club_league": "Tunisian Ligue 1"},
        {"name": "Ali Elabdi", "position": "FB", "club": "Nice", "club_league": "Ligue 1"},
        {"name": "Montassar Talbi", "position": "CB", "club": "Lorient", "club_league": "Ligue 1"},
        {"name": "Omar Rekik", "position": "CB", "club": "Maribor", "club_league": "Slovenian PrvaLiga"},
        {"name": "Adam Arous", "position": "FB", "club": "Kasimpasa", "club_league": "Super Lig"},
        {"name": "Dylan Bronn", "position": "CB", "club": "Servette", "club_league": "Swiss Super League"},
        {"name": "Mohamed Achouri", "position": "W", "club": "Copenhagen", "club_league": "Superligaen"},
        {"name": "Elias Saad", "position": "W", "club": "Hannover 96", "club_league": "Bundesliga"},
        {"name": "Hazem Mastouri", "position": "ST", "club": "Dynamo Makhachkala", "club_league": "RFPL"},
        {"name": "Hannibal Mejbri", "position": "AM", "club": "Burnley", "club_league": "Premier League"},
        {"name": "Ismael Gharbi", "position": "CM", "club": "Augsburg", "club_league": "Bundesliga"},
        {"name": "Ahmed Ben Ouanes", "position": "FB", "club": "Kasimpasa", "club_league": "Super Lig"},
        {"name": "Rani Khedira", "position": "CM", "club": "Union Berlin", "club_league": "Bundesliga"},
        {"name": "Khalil Ayari", "position": "CM", "club": "PSG", "club_league": "Ligue 1"},
        {"name": "Mohamed Belhadj", "position": "CM", "club": "Lugano", "club_league": "Swiss Super League"},
        {"name": "Aymen Dahmen", "position": "GK", "club": "CS Sfaxien", "club_league": "Tunisian Ligue 1"},
        {"name": "Ellyes Skhiri", "position": "CM", "club": "Ein Frankfurt", "club_league": "Bundesliga"},
        {"name": "Rayan Elloumi", "position": "W", "club": "Vancouver Whitecaps", "club_league": "MLS"},
        {"name": "Firas Chaouat", "position": "ST", "club": "Club Africain", "club_league": "Tunisian Ligue 1"},
        {"name": "Yan Valery", "position": "FB", "club": "Young Boys", "club_league": "Swiss Super League"},
        {"name": "Amine Ben Hamida", "position": "CB", "club": "Esperance", "club_league": "Tunisian Ligue 1"},
        {"name": "Sabri Ben Hsan", "position": "GK", "club": "Etoile du Sahel", "club_league": "Tunisian Ligue 1"},
        {"name": "Moutaz Neffati", "position": "CB", "club": "IFK Norrkoping", "club_league": "Allsvenskan"},
        {"name": "Raed Chikhaoui", "position": "CB", "club": "US Monastir", "club_league": "Tunisian Ligue 1"},
        {"name": "Anis Ben Slimane", "position": "CM", "club": "Norwich", "club_league": "EFL Championship"},
        {"name": "Sebastian Tounekti", "position": "CM", "club": "Celtic", "club_league": "Scottish Premiership"},
    ],
    "Turkey": [
        {"name": "Mert Gunok", "position": "GK", "club": "Fenerbahce", "club_league": "Super Lig"},
        {"name": "Zeki Celik", "position": "FB", "club": "Roma", "club_league": "Serie A"},
        {"name": "Merih Demiral", "position": "CB", "club": "Al-Ahli", "club_league": "SPL"},
        {"name": "Caglar Soyuncu", "position": "CB", "club": "Fenerbahce", "club_league": "Super Lig"},
        {"name": "Salih Ozcan", "position": "CM", "club": "Dortmund", "club_league": "Bundesliga"},
        {"name": "Orkun Kokcu", "position": "CM", "club": "Besiktas", "club_league": "Super Lig"},
        {"name": "Kerem Akturkoglu", "position": "W", "club": "Fenerbahce", "club_league": "Super Lig"},
        {"name": "Arda Guler", "position": "AM", "club": "Real Madrid", "club_league": "La Liga"},
        {"name": "Deniz Gul", "position": "ST", "club": "Porto", "club_league": "Liga Portugal"},
        {"name": "Hakan Calhanoglu", "position": "CM", "club": "Inter Milan", "club_league": "Serie A"},
        {"name": "Kenan Yildiz", "position": "ST", "club": "Juventus", "club_league": "Serie A"},
        {"name": "Altay Bayindir", "position": "GK", "club": "Manchester United", "club_league": "Premier League"},
        {"name": "Eren Elmali", "position": "FB", "club": "Galatasaray", "club_league": "Super Lig"},
        {"name": "Abdulkerim Bardakci", "position": "CB", "club": "Galatasaray", "club_league": "Super Lig"},
        {"name": "Ozan Kabak", "position": "CB", "club": "Hoffenheim", "club_league": "Bundesliga"},
        {"name": "Ismail Yuksek", "position": "CM", "club": "Fenerbahce", "club_league": "Super Lig"},
        {"name": "Irfan Kahveci", "position": "W", "club": "Kasimpasa", "club_league": "Super Lig"},
        {"name": "Mert Muldur", "position": "FB", "club": "Fenerbahce", "club_league": "Super Lig"},
        {"name": "Yunus Akgun", "position": "W", "club": "Galatasaray", "club_league": "Super Lig"},
        {"name": "Ferdi Kadioglu", "position": "FB", "club": "Brighton", "club_league": "Premier League"},
        {"name": "Baris Alper Yilmaz", "position": "W", "club": "Galatasaray", "club_league": "Super Lig"},
        {"name": "Kaan Ayhan", "position": "CM", "club": "Galatasaray", "club_league": "Super Lig"},
        {"name": "Ugurcan Cakir", "position": "GK", "club": "Galatasaray", "club_league": "Super Lig"},
        {"name": "Oguz Aydin", "position": "W", "club": "Fenerbahce", "club_league": "Super Lig"},
        {"name": "Samet Akaydin", "position": "CB", "club": "Ajax", "club_league": "Eredivisie"},
        {"name": "Can Uzun", "position": "ST", "club": "Ein Frankfurt", "club_league": "Bundesliga"},
    ],
    "United States": [
        {"name": "Matt Turner", "position": "GK", "club": "New England Revolution", "club_league": "MLS"},
        {"name": "Sergino Dest", "position": "FB", "club": "PSV", "club_league": "Eredivisie"},
        {"name": "Chris Richards", "position": "CB", "club": "Crystal Palace", "club_league": "Premier League"},
        {"name": "Tyler Adams", "position": "DM", "club": "Bournemouth", "club_league": "Premier League"},
        {"name": "Antonee Robinson", "position": "FB", "club": "Fulham", "club_league": "Premier League"},
        {"name": "Auston Trusty", "position": "CB", "club": "Celtic", "club_league": "Scottish Premiership"},
        {"name": "Giovanni Reyna", "position": "AM", "club": "M'gladbach", "club_league": "Bundesliga"},
        {"name": "Weston McKennie", "position": "CM", "club": "Juventus", "club_league": "Serie A"},
        {"name": "Ricardo Pepi", "position": "ST", "club": "PSV", "club_league": "Eredivisie"},
        {"name": "Christian Pulisic", "position": "W", "club": "AC Milan", "club_league": "Serie A"},
        {"name": "Brenden Aaronson", "position": "W", "club": "Leeds", "club_league": "Premier League"},
        {"name": "Miles Robinson", "position": "CB", "club": "FC Cincinnati", "club_league": "MLS"},
        {"name": "Tim Ream", "position": "CB", "club": "Charlotte FC", "club_league": "MLS"},
        {"name": "Sebastian Berhalter", "position": "CM", "club": "Vancouver Whitecaps", "club_league": "MLS"},
        {"name": "Cristian Roldan", "position": "CM", "club": "Seattle Sounders", "club_league": "MLS"},
        {"name": "Alexander Freeman", "position": "FB", "club": "Villarreal", "club_league": "La Liga"},
        {"name": "Malik Tillman", "position": "AM", "club": "Bayer Leverkusen", "club_league": "Bundesliga"},
        {"name": "Maximilian Arfsten", "position": "FB", "club": "Columbus Crew", "club_league": "MLS"},
        {"name": "Haji Wright", "position": "ST", "club": "Coventry", "club_league": "EFL Championship"},
        {"name": "Folarin Balogun", "position": "ST", "club": "Monaco", "club_league": "Ligue 1"},
        {"name": "Tim Weah", "position": "W", "club": "Marseille", "club_league": "Ligue 1"},
        {"name": "Mark McKenzie", "position": "CB", "club": "Toulouse", "club_league": "Ligue 1"},
        {"name": "Joe Scally", "position": "FB", "club": "M'gladbach", "club_league": "Bundesliga"},
        {"name": "Matt Freese", "position": "GK", "club": "New York City FC", "club_league": "MLS"},
        {"name": "Chris Brady", "position": "GK", "club": "Chicago Fire", "club_league": "MLS"},
        {"name": "Alejandro Zendejas", "position": "W", "club": "Club America", "club_league": "Liga MX"},
    ],
    "Uruguay": [
        {"name": "Sergio Rochet", "position": "GK", "club": "Internacional", "club_league": "Brasileirao"},
        {"name": "Jose Gimenez", "position": "CB", "club": "Atletico Madrid", "club_league": "La Liga"},
        {"name": "Sebastian Caceres", "position": "CB", "club": "Club America", "club_league": "Liga MX"},
        {"name": "Ronald Araujo", "position": "CB", "club": "Barcelona", "club_league": "La Liga"},
        {"name": "Manuel Ugarte", "position": "DM", "club": "Manchester United", "club_league": "Premier League"},
        {"name": "Rodrigo Bentancur", "position": "CM", "club": "Tottenham", "club_league": "Premier League"},
        {"name": "Nicolas De La Cruz", "position": "CM", "club": "Flamengo", "club_league": "Brasileirao"},
        {"name": "Federico Valverde", "position": "CM", "club": "Real Madrid", "club_league": "La Liga"},
        {"name": "Darwin Nunez", "position": "ST", "club": "Al-Hilal", "club_league": "SPL"},
        {"name": "Giorgian De Arrascaeta", "position": "AM", "club": "Flamengo", "club_league": "Brasileirao"},
        {"name": "Facundo Pellistri", "position": "W", "club": "Panathinaikos", "club_league": "Super League"},
        {"name": "Santiago Mele", "position": "GK", "club": "Monterrey", "club_league": "Liga MX"},
        {"name": "Guillermo Varela", "position": "FB", "club": "Flamengo", "club_league": "Brasileirao"},
        {"name": "Agustin Canobbio", "position": "W", "club": "Fluminense", "club_league": "Brasileirao"},
        {"name": "Emiliano Martinez Toranza", "position": "CM", "club": "Palmeiras", "club_league": "Brasileirao"},
        {"name": "Mathias Olivera", "position": "FB", "club": "Napoli", "club_league": "Serie A"},
        {"name": "Matias Vina", "position": "FB", "club": "River Plate", "club_league": "Liga Profesional"},
        {"name": "Brian Rodriguez", "position": "W", "club": "Club America", "club_league": "Liga MX"},
        {"name": "Rodrigo Aguirre", "position": "ST", "club": "Tigres UANL", "club_league": "Liga MX"},
        {"name": "Maximiliano Araujo", "position": "CM", "club": "Sporting CP", "club_league": "Liga Portugal"},
        {"name": "Federico Vinas", "position": "ST", "club": "Real Oviedo", "club_league": "La Liga"},
        {"name": "Joaquin Piquerez", "position": "CM", "club": "Palmeiras", "club_league": "Brasileirao"},
        {"name": "Fernando Muslera", "position": "GK", "club": "Estudiantes LP", "club_league": "Liga Profesional"},
        {"name": "Santiago Bueno", "position": "CB", "club": "Wolves", "club_league": "Premier League"},
        {"name": "Juan Sanabria", "position": "CM", "club": "Real Salt Lake", "club_league": "MLS"},
        {"name": "Rodrigo Zalazar", "position": "CM", "club": "Braga", "club_league": "Liga Portugal"},
    ],
    "Uzbekistan": [
        {"name": "Utkir Yusupov", "position": "GK", "club": "Navbahor", "club_league": "Uzbekistan Super League"},
        {"name": "Abdukodir Khusanov", "position": "CB", "club": "Manchester City", "club_league": "Premier League"},
        {"name": "Khojiakbar Alijonov", "position": "CB", "club": "Pakhtakor", "club_league": "Uzbekistan Super League"},
        {"name": "Farrukh Sayfiev", "position": "CB", "club": "Neftchi", "club_league": "Uzbekistan Super League"},
        {"name": "Rustamjon Ashurmatov", "position": "CB", "club": "Esteghlal", "club_league": "Persian Gulf Pro League"},
        {"name": "Akmal Mozgovoy", "position": "CM", "club": "Pakhtakor", "club_league": "Uzbekistan Super League"},
        {"name": "Otabek Shukurov", "position": "CM", "club": "Baniyas", "club_league": "UAE Pro League"},
        {"name": "Jamshid Iskanderov", "position": "CM", "club": "Neftchi", "club_league": "Uzbekistan Super League"},
        {"name": "Odiljon Khamrobekov", "position": "CM", "club": "Tractor", "club_league": "Persian Gulf Pro League"},
        {"name": "Jaloliddin Masharipov", "position": "W", "club": "Esteghlal", "club_league": "Persian Gulf Pro League"},
        {"name": "Oston Urunov", "position": "CM", "club": "Persepolis", "club_league": "Persian Gulf Pro League"},
        {"name": "Abduvakhid Nematov", "position": "GK", "club": "Nasaf", "club_league": "Uzbekistan Super League"},
        {"name": "Sherzod Nasrullayev", "position": "CB", "club": "Nasaf", "club_league": "Uzbekistan Super League"},
        {"name": "Eldor Shomurodov", "position": "ST", "club": "Istanbul Basaksehir", "club_league": "Super Lig"},
        {"name": "Umar Eshmurodov", "position": "CB", "club": "Nasaf", "club_league": "Uzbekistan Super League"},
        {"name": "Botirali Ergashev", "position": "GK", "club": "Neftchi", "club_league": "Uzbekistan Super League"},
        {"name": "Dostonbek Khamdamov", "position": "AM", "club": "Pakhtakor", "club_league": "Uzbekistan Super League"},
        {"name": "Abdulla Abdullayev", "position": "CB", "club": "Dibba", "club_league": "UAE Pro League"},
        {"name": "Azizjon Ganiyev", "position": "CM", "club": "Al Bataeh", "club_league": "UAE Pro League"},
        {"name": "Azizbek Amonov", "position": "ST", "club": "Samarkand Dinamo", "club_league": "Uzbekistan Super League"},
        {"name": "Igor Sergeev", "position": "ST", "club": "Persepolis", "club_league": "Persian Gulf Pro League"},
        {"name": "Abbosbek Fayzullaev", "position": "W", "club": "Istanbul Basaksehir", "club_league": "Super Lig"},
        {"name": "Sherzod Esanov", "position": "CM", "club": "Bukhara", "club_league": "Uzbekistan Super League"},
        {"name": "Behruzjon Karimov", "position": "CB", "club": "Surkhon", "club_league": "Uzbekistan Super League"},
        {"name": "Avazbek Ulmasaliyev", "position": "CB", "club": "AGMK", "club_league": "Uzbekistan Super League"},
        {"name": "Jakhongir Urozov", "position": "CB", "club": "Eyupspor", "club_league": "Super Lig"},
    ],
}

# ── Big-5 league helpers ──────────────────────────────────────────────────

BIG5_LEAGUES = {
    "Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1",
}

BIG5_LEAGUE_ALIASES: dict[str, str] = {
    "Premier League": "ENG-Premier League",
    "La Liga": "ESP-La Liga",
    "Bundesliga": "GER-Bundesliga",
    "Serie A": "ITA-Serie A",
    "Ligue 1": "FRA-Ligue 1",
}

LEAGUE_PROXY_RATINGS: dict[str, float] = {
    "Premier League": 61.0,
    "La Liga": 60.5,
    "Bundesliga": 58.5,
    "Serie A": 58.0,
    "Ligue 1": 56.0,
    "Liga Portugal": 53.0,
    "Eredivisie": 52.5,
    "Belgian Pro League": 49.5,
    "Jupiler Pro League": 49.5,
    "Championship": 47.0,
    "EFL Championship": 47.0,
    "Scottish Premiership": 46.5,
    "Scottish Premiership ": 46.5,
    "MLS": 49.0,
    "Brasileirao": 51.5,
    "Super Lig": 48.0,
    "SPL": 50.5,
    "Saudi Pro League": 50.5,
    "A-League": 41.0,
    "J-League": 44.0,
    "Swiss Super League": 46.0,
    "Austrian Bundesliga": 47.0,
    "Danish Superliga": 46.0,
    "Eliteserien": 44.5,
    "HNL": 44.5,
    "NB I": 42.0,
    "RFPL": 47.0,
    "Qatar Stars League": 40.5,
    "Persian Gulf Pro League": 39.5,
    "UAE Pro League": 39.0,
    "K League 1": 42.0,
    "K-League": 42.0,
    "Jupiler Pro League ": 49.5,
}


# ── Squad access helpers ──────────────────────────────────────────────────

def get_all_teams() -> list[str]:
    """Return all 48 World Cup team names."""
    teams: list[str] = []
    for group_teams in GROUPS.values():
        teams.extend(group_teams)
    return teams


def get_team_group(team: str) -> str | None:
    """Return the group letter for a team, or None if not found."""
    for letter, teams in GROUPS.items():
        if team in teams:
            return letter
    return None


def get_squad(team: str) -> list[SquadPlayer]:
    """Return the squad for a team as a list of SquadPlayer dataclasses."""
    raw = SQUADS.get(team, [])
    return [
        SquadPlayer(
            name=p["name"],
            position=p["position"],
            club=p["club"],
            club_league=p["club_league"],
        )
        for p in raw
    ]


def is_big5_league(league_name: str) -> bool:
    """Check if a league name is a Big-5 European league."""
    return league_name in BIG5_LEAGUES or league_name in BIG5_LEAGUE_ALIASES


def league_proxy_rating(league_name: str) -> float:
    """Return a proxy player rating for leagues without direct player scores."""
    if league_name in LEAGUE_PROXY_RATINGS:
        return LEAGUE_PROXY_RATINGS[league_name]
    if is_big5_league(league_name):
        return 58.0
    if "League One" in league_name or "League Two" in league_name:
        return 38.0
    if "Super League" in league_name:
        return 43.0
    if "Pro League" in league_name:
        return 42.0
    if "Bundesliga" in league_name:
        return 46.0
    return 42.0


def enrich_squad_with_ratings(
    squad: list[SquadPlayer],
    ratings_df,  # pd.DataFrame
) -> list[SquadPlayer]:
    """Enrich squad players with ratings from the optimized ratings data.

    Matches by player name (exact -> case-insensitive -> last-name substring).
    Sets has_rating, rating, and rating_confidence fields.
    """
    import pandas as pd

    if ratings_df.empty:
        return squad

    # Determine the player name column
    name_col = "player" if "player" in ratings_df.columns else "player_name"
    if name_col not in ratings_df.columns:
        return squad

    # Prefer the latest season (2526) for matching, but allow all seasons
    season_col = "season" if "season" in ratings_df.columns else None

    for player in squad:
        match = pd.DataFrame()

        # Try exact name match first
        exact = ratings_df[ratings_df[name_col] == player.name]
        if not exact.empty:
            match = exact
        else:
            # Try case-insensitive match
            ci = ratings_df[
                ratings_df[name_col].str.lower() == player.name.lower()
            ]
            if not ci.empty:
                match = ci
            else:
                # Try last name match (common for transliterated names)
                last_name = player.name.split()[-1]
                ln = ratings_df[
                    ratings_df[name_col].str.lower().str.contains(
                        last_name.lower(), na=False
                    )
                ]
                if not ln.empty:
                    match = ln

        if not match.empty:
            # Prefer 2526 season if available
            if season_col and "2526" in match[season_col].values:
                row = match[match[season_col] == "2526"].iloc[0]
            else:
                row = match.iloc[0]

            score = row.get("optimized_score")
            if pd.notna(score):
                player.has_rating = True
                player.rating = float(score)
                # Confidence based on league coverage
                league = str(row.get("league", ""))
                if is_big5_league(league):
                    player.rating_confidence = "high"
                else:
                    player.rating_confidence = "medium"

    return squad


def enrich_squads_with_ratings(
    ratings_df,  # pd.DataFrame
) -> dict[str, list[SquadPlayer]]:
    """Enrich all WC squads with ratings from player_ratings_optimized.parquet.

    Returns a dict of team_name -> list[SquadPlayer] with rating data filled in.
    """
    result: dict[str, list[SquadPlayer]] = {}
    for team_name in get_all_teams():
        squad = get_squad(team_name)
        result[team_name] = enrich_squad_with_ratings(squad, ratings_df)
    return result


def compute_team_strengths(
    enriched_squads: dict[str, list[SquadPlayer]] | None = None,
    ratings_df=None,  # pd.DataFrame | None
) -> dict[str, float]:
    """Compute a strength score for each World Cup team."""
    details = compute_team_strength_details(
        enriched_squads=enriched_squads,
        ratings_df=ratings_df,
    )
    return {team: values["strength"] for team, values in details.items()}


def compute_team_strength_details(
    enriched_squads: dict[str, list[SquadPlayer]] | None = None,
    ratings_df=None,  # pd.DataFrame | None
) -> dict[str, dict[str, float]]:
    """Compute strength score plus interpretable components for each team."""
    if enriched_squads is None:
        if ratings_df is None:
            from scoutfootball.app.data_loader import load_player_ratings
            ratings_df = load_player_ratings()
        enriched_squads = enrich_squads_with_ratings(ratings_df)

    strengths: dict[str, dict[str, float]] = {}

    for team_name, squad in enriched_squads.items():
        rated = [p for p in squad if p.has_rating]
        coverage = len(rated) / len(squad) if squad else 0.0

        observed_avg = (
            sum(p.rating for p in rated if p.rating is not None) / len(rated)
            if rated else 43.0
        )
        proxy_scores = [league_proxy_rating(p.club_league) for p in squad]
        proxy_avg = sum(proxy_scores) / len(proxy_scores) if proxy_scores else 42.0
        shrunk_avg = coverage * observed_avg + (1 - coverage) * proxy_avg

        imputed_scores = [
            float(p.rating) if p.has_rating and p.rating is not None else league_proxy_rating(p.club_league)
            for p in squad
        ]
        imputed_scores.sort(reverse=True)
        core = imputed_scores[:11]
        depth = imputed_scores[11:18]
        reserve = imputed_scores[18:]
        core_avg = sum(core) / len(core) if core else shrunk_avg
        depth_avg = sum(depth) / len(depth) if depth else core_avg
        reserve_avg = sum(reserve) / len(reserve) if reserve else depth_avg

        squad_quality = (
            0.55 * core_avg
            + 0.20 * depth_avg
            + 0.10 * reserve_avg
            + 0.15 * shrunk_avg
        )
        rating_score = min(max((squad_quality - 30) / 40, 0), 1)

        opta_score = OPTA_WIN_PROBABILITY.get(team_name, 0.01)
        opta_normalized = min(opta_score / 0.16, 1.0)

        big5_count = sum(1 for p in squad if p.club_league in BIG5_LEAGUES)
        big5_ratio = big5_count / len(squad) if squad else 0.0
        big5_score = min(big5_ratio / 0.6, 1.0)
        league_score = min(max((proxy_avg - 35) / 25, 0), 1)
        coverage_score = coverage ** 0.7

        strength = (
            0.46 * rating_score
            + 0.24 * opta_normalized
            + 0.18 * league_score
            + 0.07 * coverage_score
            + 0.05 * big5_score
        )
        if team_name in HOSTS:
            strength = min(strength + 0.04, 1.0)  # ~4% host bonus, capped at 1.0
        strengths[team_name] = {
            "strength": round(strength, 4),
            "coverage": round(coverage, 4),
            "observed_avg_rating": round(observed_avg, 2),
            "proxy_avg_rating": round(proxy_avg, 2),
            "shrunk_avg_rating": round(shrunk_avg, 2),
            "core_avg_rating": round(core_avg, 2),
            "depth_avg_rating": round(depth_avg, 2),
            "reserve_avg_rating": round(reserve_avg, 2),
            "squad_quality_rating": round(squad_quality, 2),
            "rating_score": round(rating_score, 4),
            "opta_score": round(opta_normalized, 4),
            "league_score": round(league_score, 4),
            "coverage_score": round(coverage_score, 4),
            "big5_score": round(big5_score, 4),
            "big5_ratio": round(big5_ratio, 4),
        }

    return strengths


def compute_group_predictions(
    team_strengths: dict[str, float],
) -> list[dict]:
    """Estimate group advancement probabilities for all groups.

    Uses a strength-ratio model with exponential amplification (k=2.5)
    to differentiate strong and weak teams. Returns a list of group dicts,
    each containing group letter, teams with their advancement probabilities.
    """
    _amplification = 2.5  # exponent to widen gap between strong/weak teams
    results = []
    for letter, teams in GROUPS.items():
        team_strength_pairs = [
            (t, team_strengths.get(t, 0.2)) for t in teams
        ]
        # Amplify strengths to widen probability gaps
        amplified = [(t, s ** _amplification) for t, s in team_strength_pairs]
        total = sum(s for _, s in amplified)

        group_teams = []
        for (team, _raw_strength), (_, strength) in zip(team_strength_pairs, amplified, strict=True):
            p1 = strength / total if total > 0 else 0.25
            # p2nd: sum over each other team j being 1st, prob i is best of remaining
            p2 = 0.0
            for other_team, other_strength in amplified:
                if other_team == team:
                    continue
                p1_other = other_strength / total if total > 0 else 0
                remaining = total - other_strength
                p2 += p1_other * (strength / remaining if remaining > 0 else 0)
            # p3rd: sum over each pair (j, k) being 1st and 2nd, prob i is best of remaining
            p3 = 0.0
            for j_team, j_strength in amplified:
                if j_team == team:
                    continue
                p1_j = j_strength / total if total > 0 else 0
                remaining_after_j = total - j_strength
                for k_team, k_strength in amplified:
                    if k_team == team or k_team == j_team:
                        continue
                    p2_jk = p1_j * (k_strength / remaining_after_j if remaining_after_j > 0 else 0)
                    remaining_after_jk = total - j_strength - k_strength
                    p3 += p2_jk * (strength / remaining_after_jk if remaining_after_jk > 0 else 0)
            p4 = max(1 - p1 - p2 - p3, 0)
            # 8 of 12 third-place teams advance to knockout
            p_advance = min(p1 + p2 + p3 * (8 / 12), 1.0)
            group_teams.append({
                "team": team,
                "strength": round(_raw_strength, 3),
                "p1st": round(p1, 3),
                "p2nd": round(p2, 3),
                "p3rd": round(p3, 3),
                "p4th": round(p4, 3),
                "p_advance": round(p_advance, 3),
            })

        group_teams.sort(key=lambda x: x["strength"], reverse=True)
        results.append({
            "group": letter,
            "teams": group_teams,
        })

    return results


# ── Knockout bracket simulation ─────────────────────────────────────────


def _knockout_match_prob(
    home_strength: float, away_strength: float, *, k: float = 2.8
) -> float:
    """Return probability that the home team wins a knockout match.

    Uses a Bradley-Terry-like model with amplification exponent *k*.
    In knockout rounds there is no draw; if the match is level after
    extra time the winner is decided by penalties, so we fold the
    draw probability into a coin-flip for evenly matched teams.
    """
    if home_strength <= 0 and away_strength <= 0:
        return 0.5
    hs = max(home_strength, 1e-6) ** k
    as_ = max(away_strength, 1e-6) ** k
    return hs / (hs + as_)


def _predict_group_finishes(
    group_predictions: list[dict],
) -> tuple[list[tuple[str, str, float]], list[tuple[str, str, float]], list[tuple[str, str, float]]]:
    """Return (first, second, third) lists of (group, team, strength) sorted by strength.

    Each group prediction is expected to have ``group`` and ``teams`` keys,
    where each team has ``team``, ``strength``, ``p1st``, ``p2nd``, ``p3rd``.
    The most likely finishing order (1st/2nd/3rd) is derived from the
    probabilities.
    """
    firsts: list[tuple[str, str, float]] = []
    seconds: list[tuple[str, str, float]] = []
    thirds: list[tuple[str, str, float]] = []
    for gp in group_predictions:
        letter = gp["group"]
        teams = list(gp["teams"])
        if not teams:
            continue
        # Pick the most likely 1st, then 2nd, then 3rd
        ranked = sorted(teams, key=lambda t: (-t.get("p1st", 0), -t.get("strength", 0)))
        if len(ranked) >= 1:
            t = ranked[0]
            firsts.append((letter, t["team"], t.get("strength", 0.2)))
        if len(ranked) >= 2:
            t = ranked[1]
            seconds.append((letter, t["team"], t.get("strength", 0.2)))
        if len(ranked) >= 3:
            t = ranked[2]
            thirds.append((letter, t["team"], t.get("strength", 0.2)))
    return firsts, seconds, thirds


def _seed_round_of_32(
    firsts: list[tuple[str, str, float]],
    seconds: list[tuple[str, str, float]],
    thirds: list[tuple[str, str, float]],
) -> list[tuple[str, str, float, str, str, float]]:
    """Create 16 Round-of-32 matchups as (home_group, home_team, home_str, away_group, away_team, away_str).

    The 2026 World Cup has 12 group winners + 12 runners-up + 8 best
    third-placed teams = 32 teams. The official bracket pairs winners
    against runners-up/thirds from specific groups, but the exact third-
    place assignment depends on which groups the best thirds come from.

    We use a simplified but fair seeding: group winners are seeded by
    strength and paired against runners-up/thirds by a complementary
    seed, so that strong winners are not paired together early.
    """
    # Sort winners by strength descending
    winners = sorted(firsts, key=lambda x: -x[2])
    # Sort runners-up by strength descending
    runners = sorted(seconds, key=lambda x: -x[2])
    # Best 8 third-placed teams by strength
    best_thirds = sorted(thirds, key=lambda x: -x[2])[:8]

    # Build the 32-team pool: 12 winners + 12 runners-up + 8 thirds = 32
    # Seeds 1-12 = winners (by strength), 13-24 = runners-up, 25-32 = thirds
    seeded: list[tuple[str, str, float]] = []
    seeded.extend(winners)
    seeded.extend(runners)
    seeded.extend(best_thirds)

    # Standard bracket: seed 1 vs seed 32, 2 vs 31, etc.
    n = len(seeded)
    matchups: list[tuple[str, str, float, str, str, float]] = []
    for i in range(n // 2):
        home = seeded[i]
        away = seeded[n - 1 - i]
        matchups.append((home[0], home[1], home[2], away[0], away[1], away[2]))
    return matchups


def simulate_knockout(
    team_strengths: dict[str, float],
    group_predictions: list[dict] | None = None,
    *,
    num_simulations: int = 10000,
    seed: int = 42,
) -> dict:
    """Simulate the World Cup knockout bracket and return round-by-round probabilities.

    Parameters
    ----------
    team_strengths:
        Mapping of team name → strength score (0-1 scale).
    group_predictions:
        Optional pre-computed group predictions from
        :func:`compute_group_predictions`. If ``None``, will be computed
        from *team_strengths*.
    num_simulations:
        Number of Monte Carlo simulations for tournament win probability.
    seed:
        Random seed for reproducibility.

    Returns
    -------
    dict with keys:
        - ``round_of_32``: list of 16 matchups, each with home/away teams,
          strengths, and win probability.
        - ``round_of_16``: list of 8 projected matchups with advancement
          probabilities (most likely winner).
        - ``quarter_finals``: list of 4 projected matchups.
        - ``semi_finals``: list of 2 projected matchups.
        - ``final``: the projected final matchup.
        - ``tournament_win_probability``: list of all 48 teams with their
          probability of winning the tournament (sorted descending).
        - ``disclaimer``: limitations notice.
    """
    import random

    rng = random.Random(seed)

    if group_predictions is None:
        group_predictions = compute_group_predictions(team_strengths)

    firsts, seconds, thirds = _predict_group_finishes(group_predictions)
    r32_matchups = _seed_round_of_32(firsts, seconds, thirds)

    # ── Round of 32 matchups with probabilities ──
    r32: list[dict] = []
    for hg, ht, hs, ag, at_, as_ in r32_matchups:
        p_home = _knockout_match_prob(hs, as_)
        r32.append({
            "home_group": hg,
            "home_team": ht,
            "home_strength": round(hs, 4),
            "away_group": ag,
            "away_team": at_,
            "away_strength": round(as_, 4),
            "home_win_probability": round(p_home, 4),
            "away_win_probability": round(1 - p_home, 4),
        })

    # ── Project subsequent rounds by picking most likely winners ──
    def _project_round(prev_matchups: list[dict]) -> list[dict]:
        """Project the next round by advancing the most likely winner from each pair."""
        next_matchups: list[dict] = []
        for i in range(0, len(prev_matchups), 2):
            if i + 1 >= len(prev_matchups):
                break
            m1 = prev_matchups[i]
            m2 = prev_matchups[i + 1]
            # Pick most likely winners
            w1 = m1["home_team"] if m1["home_win_probability"] >= 0.5 else m1["away_team"]
            w1_str = m1["home_strength"] if m1["home_win_probability"] >= 0.5 else m1["away_strength"]
            w2 = m2["home_team"] if m2["home_win_probability"] >= 0.5 else m2["away_team"]
            w2_str = m2["home_strength"] if m2["home_win_probability"] >= 0.5 else m2["away_strength"]
            p_w1 = _knockout_match_prob(w1_str, w2_str)
            next_matchups.append({
                "home_team": w1,
                "home_strength": round(w1_str, 4),
                "away_team": w2,
                "away_strength": round(w2_str, 4),
                "home_win_probability": round(p_w1, 4),
                "away_win_probability": round(1 - p_w1, 4),
                "from_match": [i + 1, i + 2],
            })
        return next_matchups

    r16 = _project_round(r32)
    qf = _project_round(r16)
    sf = _project_round(qf)
    final = _project_round(sf)

    # ── Monte Carlo tournament win probability ──
    # Simulate the full bracket num_simulations times
    win_counts: dict[str, int] = {team: 0 for team in team_strengths}
    sim_count = 0

    for _ in range(num_simulations):
        # Start with the Round of 32 teams
        current_teams: list[tuple[str, float]] = []
        for m in r32_matchups:
            hg, ht, hs, ag, at_, as_ = m
            p_home = _knockout_match_prob(hs, as_)
            if rng.random() < p_home:
                current_teams.append((ht, hs))
            else:
                current_teams.append((at_, as_))

        # Simulate rounds until one team remains
        while len(current_teams) > 1:
            next_round: list[tuple[str, float]] = []
            for i in range(0, len(current_teams) - 1, 2):
                t1, s1 = current_teams[i]
                t2, s2 = current_teams[i + 1]
                p1 = _knockout_match_prob(s1, s2)
                if rng.random() < p1:
                    next_round.append((t1, s1))
                else:
                    next_round.append((t2, s2))
            current_teams = next_round

        if current_teams:
            winner = current_teams[0][0]
            win_counts[winner] = win_counts.get(winner, 0) + 1
            sim_count += 1

    # Build tournament win probability list
    tournament_win_prob: list[dict] = []
    for team, strength in sorted(team_strengths.items(), key=lambda x: -x[1]):
        p = win_counts.get(team, 0) / sim_count if sim_count > 0 else 0.0
        tournament_win_prob.append({
            "team": team,
            "group": get_team_group(team),
            "strength": round(strength, 4),
            "win_probability": round(p, 4),
        })
    tournament_win_prob.sort(key=lambda x: -x["win_probability"])

    return {
        "status": "ok",
        "round_of_32": r32,
        "round_of_16": r16,
        "quarter_finals": qf,
        "semi_finals": sf,
        "final": final,
        "tournament_win_probability": tournament_win_prob[:16],
        "num_simulations": num_simulations,
        "disclaimer": (
            "Knockout probabilities use a simplified Bradley-Terry strength "
            "model. Real match outcomes depend on form, injuries, tactics "
            "and home-field advantage not captured here. Non-Big5 league "
            "team strengths may be underestimated."
        ),
    }
