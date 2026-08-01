from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

MODELS_CSV = DATA_DIR / "models.csv"
SPECS_CSV = DATA_DIR / "specifications.csv"
GROUPS_CSV = DATA_DIR / "catalogs.csv"
CATALOGS_CSV = GROUPS_CSV
PARTS_CSV = DATA_DIR / "parts.csv"

START_YEAR = 2016
END_YEAR = 2026

SAVE_AFTER = 50

HEADLESS = False

REQUEST_DELAY_MIN = 0.0
REQUEST_DELAY_MAX = 0.0

STATUS_PENDING = "PENDING"
STATUS_DONE = "DONE"
STATUS_FAILED = "FAILED"

SPEC_COLUMNS = [
    "model",
    "year",
    "destination",
    "specification_name",
    "description",
    "variant",
    "options",
    "production_period",
    "url",
    "status",
]

SPECS_COLUMNS = SPEC_COLUMNS
SPECS_COLUMNS = SPEC_COLUMNS

GROUP_COLUMNS = [
    "model",
    "year",
    "destination",
    "specification_name",
    "category_code",
    "category_name",
    "url",
    "status",
]
CATALOGS_COLUMNS = GROUP_COLUMNS

PART_COLUMNS = [
    "car_name",
    "model",
    "chassis",
    "year",
    "destination",
    "description",
    "options",
    "production_period",
    "category",
    "oem_number",
    "part_name",
    "part_code",
    "part_note",
    "quantity",
    "part_range",
    "source_url",
]

DESTINATIONS = {
    "CHINA": "CHINA",
    "SOUTH KOREA": "SOUTH KOREA",
    "TAIWAN": "TAIWAN",
    "HONG KONG": "HONG KONG",
    "MONGOLIA": "MONGOLIA",
    "THAILAND": "THAILAND",
    "INDONESIA": "INDONESIA",
    "MALAYSIA": "MALAYSIA",
    "PHILIPPINES": "PHILIPPINES",
    "VIETNAM": "VIETNAM",
    "SINGAPORE": "SINGAPORE",
    "BRUNEI": "BRUNEI",
    "MYANMAR": "MYANMAR",
    "CAMBODIA": "CAMBODIA",
    "LAOS": "LAOS",
    "TIMOR-LESTE": "TIMOR-LESTE",
    "INDIA": "INDIA",
    "PAKISTAN": "PAKISTAN",
    "BANGLADESH": "BANGLADESH",
    "SRI LANKA": "SRI LANKA",
    "NEPAL": "NEPAL",
    "BHUTAN": "BHUTAN",
    "MALDIVES": "MALDIVES",
    "KAZAKHSTAN": "KAZAKHSTAN",
    "UZBEKISTAN": "UZBEKISTAN",
    "TURKMENISTAN": "TURKMENISTAN",
    "TAJIKISTAN": "TAJIKISTAN",
    "KYRGYZSTAN": "KYRGYZSTAN",
    "AZERBAIJAN": "AZERBAIJAN",
    "GEORGIA": "GEORGIA",
    "ARMENIA": "ARMENIA",
    "IRAQ": "IRAQ",
    "JORDAN": "JORDAN",
    "LEBANON": "LEBANON",
    "ISRAEL": "ISRAEL",
    "YEMEN": "YEMEN",
    "GULF CORPORATION COUNCIL": "GULF CORPORATION COUNCIL",
    "FOR CHINA": "FOR CHINA",
    "FOR SOUTH KOREA": "FOR SOUTH KOREA",
    "FOR TAIWAN": "FOR TAIWAN",
    "FOR HONG KONG": "FOR HONG KONG",
    "FOR MONGOLIA": "FOR MONGOLIA",
    "FOR THAILAND": "FOR THAILAND",
    "FOR INDONESIA": "FOR INDONESIA",
    "FOR MALAYSIA": "FOR MALAYSIA",
    "FOR PHILIPPINES": "FOR PHILIPPINES",
    "FOR VIETNAM": "FOR VIETNAM",
    "FOR SINGAPORE": "FOR SINGAPORE",
    "FOR BRUNEI": "FOR BRUNEI",
    "FOR MYANMAR": "FOR MYANMAR",
    "FOR CAMBODIA": "FOR CAMBODIA",
    "FOR LAOS": "FOR LAOS",
    "FOR TIMOR-LESTE": "FOR TIMOR-LESTE",
    "FOR INDIA": "FOR INDIA",
    "FOR PAKISTAN": "FOR PAKISTAN",
    "FOR BANGLADESH": "FOR BANGLADESH",
    "FOR SRI LANKA": "FOR SRI LANKA",
    "FOR NEPAL": "FOR NEPAL",
    "FOR BHUTAN": "FOR BHUTAN",
    "FOR MALDIVES": "FOR MALDIVES",
    "FOR KAZAKHSTAN": "FOR KAZAKHSTAN",
    "FOR UZBEKISTAN": "FOR UZBEKISTAN",
    "FOR TURKMENISTAN": "FOR TURKMENISTAN",
    "FOR TAJIKISTAN": "FOR TAJIKISTAN",
    "FOR KYRGYZSTAN": "FOR KYRGYZSTAN",
    "FOR AZERBAIJAN": "FOR AZERBAIJAN",
    "FOR GEORGIA": "FOR GEORGIA",
    "FOR ARMENIA": "FOR ARMENIA",
    "FOR IRAQ": "FOR IRAQ",
    "FOR JORDAN": "FOR JORDAN",
    "FOR LEBANON": "FOR LEBANON",
    "FOR ISRAEL": "FOR ISRAEL",
    "FOR YEMEN": "FOR YEMEN",
}