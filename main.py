from lxml import html

import config

from crawler import Browser
from selenium.common.exceptions import WebDriverException

import extractor as ex


def phase_specifications(browser):
    """models.csv -> specifications.csv"""

    driver = browser.driver()
    models = ex.load_models()

    for i, row in models.iterrows():
        if row["status"] == config.STATUS_DONE:
            continue

        print("=" * 80)
        print(f"MODEL : {row['model']}")
        print(f"URL   : {row['url']}")

        attempt = 0
        success = False

        while attempt < 3 and not success:
            attempt += 1
            try:
                # ensure browser is alive
                browser.ensure_alive()

                browser.open(row["url"])
                html = browser.html()

                years = ex.get_available_years(html)
                if not years:
                    years = list(range(config.START_YEAR, config.END_YEAR + 1))

                print(f"Years Found : {years}")

                for year in years:
                    print("-" * 80)
                    print(f"YEAR : {year}")

                    try:
                        ex.select_year(driver, year)
                    except Exception as exc:
                        print(f"Skipping year {year}: {exc}")
                        continue

                    destinations = ex.whitelisted_destinations(driver)

                    print(f"Destinations Found : {len(destinations)}")

                    for destination, value in destinations.items():
                        print(f"DESTINATION : {destination}")

                        try:
                            ex.select_destination(driver, value)
                        except Exception as exc:
                            print(f"Skipping destination {destination}: {exc}")
                            continue

                        html = browser.html()
                        rows = ex.specification_links(
                            html=html,
                            model=row["model"],
                            year=year,
                            destination=destination,
                        )

                        ex.append_rows(
                            config.SPECS_CSV,
                            config.SPECS_COLUMNS,
                            rows,
                        )

                        print(f"Specifications : {len(rows)}")

                models.at[i, "status"] = config.STATUS_DONE
                success = True
            except Exception as exc:
                msg = str(exc)
                print(f"FAILED (attempt {attempt}): {msg}")
                # If this looks like a WebDriver/window problem, restart browser and retry
                if isinstance(exc, WebDriverException) or "no such window" in msg.lower() or "web view not found" in msg.lower():
                    try:
                        print("Attempting browser restart and retry...")
                        browser.restart()
                    except Exception as e:
                        print(f"Restart failed: {e}")
                    continue
                else:
                    models.at[i, "status"] = config.STATUS_FAILED
                    break
            models.at[i, "status"] = config.STATUS_FAILED

        ex.save_csv(config.MODELS_CSV, models)


def phase_catalogs(browser):
    """specifications.csv -> catalogs.csv"""

    catalogs = ex.load_specifications()

    if "status" not in catalogs.columns:
        catalogs["status"] = config.STATUS_PENDING

    for i, row in catalogs.iterrows():
        if row["status"] == config.STATUS_DONE:
            continue

        if not row["url"]:
            continue

        print("=" * 80)
        print(f"MODEL : {row['model']}")
        print(f"SPEC  : {row['specification_name']}")

        try:
            browser.open(row["url"])
            html = browser.html()

            rows = ex.category_links(
                html=html,
                model=row["model"],
                year=row["year"],
                destination=row["destination"],
                specification=row["specification_name"],
            )

            ex.append_rows(
                config.CATALOGS_CSV,
                config.CATALOGS_COLUMNS,
                rows,
            )

            print(f"Categories : {len(rows)}")
            catalogs.at[i, "status"] = config.STATUS_DONE
        except Exception as exc:
            print(f"FAILED : {exc}")
            catalogs.at[i, "status"] = config.STATUS_FAILED

        ex.save_csv(config.SPECS_CSV, catalogs)


def phase_parts(browser):
    """catalogs.csv -> parts.csv"""

    catalogs = ex.load_categories()

    if "status" not in catalogs.columns:
        catalogs["status"] = config.STATUS_PENDING

    buffer = ex.PartsBuffer()

    for i, row in catalogs.iterrows():

        if row["status"] == config.STATUS_DONE:
            continue

        if not row["url"]:
            continue

        print("=" * 80)
        print(f"MODEL       : {row['model']}")
        print(f"YEAR        : {row['year']}")
        print(f"DESTINATION : {row['destination']}")

        try:
            browser.open(row["url"])
            html = browser.html()

            parts = ex.parts_table(
                html=html,
                model=row["model"],
                year=row["year"],
                destination=row["destination"],
                source_url=row["url"],
            )

            for part in parts:
                buffer.add(part)

            buffer.flush()

            print(f"Parts scraped : {len(parts)}")

            catalogs.at[i, "status"] = config.STATUS_DONE

        except Exception as exc:
            print(f"FAILED : {exc}")
            catalogs.at[i, "status"] = config.STATUS_FAILED
            print(exc)

        ex.save_csv(config.CATALOGS_CSV, catalogs)


def main():
    with Browser() as browser:
        # phase_specifications(browser)
        # phase_catalogs(browser)
        phase_parts(browser)


if __name__ == "__main__":
    main()
