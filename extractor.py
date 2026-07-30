import csv
import re
from pathlib import Path

import pandas as pd

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from urllib.parse import urljoin

import config


BASE_URL = "https://partsouq.com"


# ============================================================================
# CSV
# ============================================================================

def load_csv(path):
    path = Path(path)

    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path)


def save_csv(path, df):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def append_rows(path, columns, rows):
    if not rows:
        return

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    file_exists = path.exists()

    with open(path, "a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)

        if not file_exists:
            writer.writeheader()

        for row in rows:
            writer.writerow(row)


def load_models():
    return load_csv(config.MODELS_CSV)


def load_specifications():
    return load_csv(config.SPECS_CSV)


def load_categories():
    return load_csv(config.CATALOGS_CSV)


# ============================================================================
# YEAR
# ============================================================================

def get_available_years(html):
    soup = BeautifulSoup(html, "lxml")

    years = []
    select = soup.select_one("#f_year")

    if select is not None:
        for option in select.select("option"):
            text = option.get_text(strip=True)
            if text.isdigit():
                years.append(int(text))

    if not years:
        text = soup.get_text(" ", strip=True)
        years = [int(match) for match in re.findall(r"\b(19\d{2}|20\d{2})\b", text)]

    return sorted({year for year in years if config.START_YEAR <= year <= config.END_YEAR})


def select_year(sb, year):
    Select(sb.find_element("#f_year")).select_by_visible_text(str(year))


# ============================================================================
# DESTINATION
# ============================================================================

def whitelisted_destinations(sb):
    select = Select(sb.find_element("#f_destination"))

    results = {}

    allowed = set(config.DESTINATIONS.keys())

    for option in select.options:
        text = option.text.strip()
        if not text:
            continue

        normalized = text.upper()
        # exact match
        if normalized in allowed:
            results[text] = option.get_attribute("value")
            continue

        # handle variants like 'FOR MALAYSIA' and substrings
        compact = normalized.replace("FOR ", "")
        if compact in allowed:
            results[text] = option.get_attribute("value")
            continue

        # substring match (either direction)
        matched = False
        for a in allowed:
            if a in normalized or normalized in a or a in compact or compact in a:
                results[text] = option.get_attribute("value")
                matched = True
                break
        if matched:
            continue

    return results


def select_destination(sb, value):
    sel = Select(sb.find_element("#f_destination"))
    try:
        sel.select_by_value(value)
        return
    except Exception:
        pass

    try:
        sel.select_by_visible_text(value)
        return
    except Exception:
        pass

    # Fallback: try to click an option that matches fuzzily
    for opt in sel.options:
        try:
            opt_val = opt.get_attribute("value")
            opt_text = (opt.text or "").strip()
            if opt_val == value or value.upper() in opt_text.upper() or opt_text.upper() in value.upper():
                try:
                    opt.click()
                    return
                except Exception:
                    continue
        except Exception:
            continue

    # If nothing matched, raise to let caller handle
    raise Exception(f"Could not select destination with value/text '{value}'")


# ============================================================================
# SPECIFICATION LINKS
# ============================================================================

def specification_links(html, model, year, destination):
    soup = BeautifulSoup(html, "lxml")

    rows = []
    seen = set()

    # Find the table containing specifications
    table = None

    for t in soup.select("table"):
        headers = [
            th.get_text(" ", strip=True).upper()
            for th in t.select("th")
        ]

        if (
            "NAME" in headers
            and "DESCRIPTION" in headers
            and "MODEL" in headers
        ):
            table = t
            break

    if table is None:
        print("Specification table not found.")
        return rows

    body = table.find("tbody") or table

    for tr in body.find_all("tr"):

        cols = tr.find_all("td")

        # Skip header/invalid rows
        if len(cols) < 5:
            continue

        a = tr.find("a", href=True)
        if a is None:
            continue

        href = str(a.get("href", ""))

        if not href:
            continue

        href = urljoin(BASE_URL, href)

        if href in seen:
            continue
        seen.add(href)

        values = [
            td.get_text(" ", strip=True)
            for td in cols
        ]

        while len(values) < 5:
            values.append("")

        rows.append(
            {
                "model": model,
                "year": year,
                "destination": destination,
                "specification_name": values[0],
                "description": values[1],
                "variant": values[2],
                "options": values[3],
                "production_period": values[4],
                "url": href,
                "status": config.STATUS_PENDING,
            }
        )

    print(f"Specifications extracted: {len(rows)}")

    return rows

# ============================================================================
# CATEGORY LINKS
# ============================================================================

def category_links(
    html,
    model,
    year,
    destination,
    specification=None,
    specification_name=None,
):
    if specification is None:
        specification = specification_name or ""

    soup = BeautifulSoup(html, "lxml")
    rows = []
    seen = set()

    for a in soup.select("a[href]"):
        href = str(a.get("href", ""))
        if not href or "/catalog/genuine/unit?" not in href:
            continue

        href = urljoin(BASE_URL, href)
        if href in seen:
            continue
        seen.add(href)

        text = " ".join(a.get_text(" ", strip=True).split())

        category_code = ""
        category_name = text

        if ":" in text:
            category_code, category_name = text.split(":", 1)
            category_code = category_code.strip()
            category_name = category_name.strip()

        rows.append(
            {
                "model": model,
                "year": year,
                "destination": destination,
                "specification_name": specification,
                "category_code": category_code,
                "category_name": category_name,
                "url": href,
                "status": config.STATUS_PENDING,
            }
        )

    return rows


# ============================================================================
# PARTS TABLE
# ============================================================================

def parts_table(
    html,
    model,
    year,
    destination,
    specification=None,
    specification_name=None,
    category_code="",
    category_name="",
):
    if specification is None:
        specification = specification_name or ""

    soup = BeautifulSoup(html, "lxml")
    table = soup.select_one("table")

    if table is None:
        return []

    rows = []
    body = table.find("tbody") or table

    for tr in body.find_all("tr"):
        cols = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if len(cols) < 6:
            continue

        rows.append(
            {
                "model": model,
                "year": year,
                "destination": destination,
                "specification_name": specification,
                "category_code": category_code,
                "category_name": category_name,
                "number": cols[0],
                "name": cols[1],
                "code": cols[2],
                "note": cols[3],
                "quantity": cols[4],
                "range": cols[5],
            }
        )

    return rows


class PartsBuffer:

    def __init__(self):
        self.rows = []

    def add(self, row):
        self.rows.append(row)

    def flush(self):
        if not self.rows:
            return

        append_rows(
            config.PARTS_CSV,
            config.PART_COLUMNS,
            self.rows,
        )
        self.rows.clear()