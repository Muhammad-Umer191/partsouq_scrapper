from seleniumbase import SB
from selenium.webdriver.support.ui import Select

URL = "https://partsouq.com/en/catalog/genuine/pick?c=Toyota&model=RAV4&ssd=%24%2AKwH2rKvP9vDyAAAAAACDXQ4%3D%24"

with SB(uc=True, headless=False) as sb:

    # --------------------------------------------------
    # Open page and bypass Cloudflare
    # --------------------------------------------------
    sb.uc_open_with_reconnect(URL, reconnect_time=8)

    try:
        sb.uc_gui_handle_captcha()
    except Exception:
        pass

    sb.wait_for_ready_state_complete()
    sb.sleep(5)

    # --------------------------------------------------
    # Select Year = 2020
    # --------------------------------------------------
    year_select = Select(sb.find_element("#f_year"))
    year_select.select_by_visible_text("2020")

    sb.sleep(2)

    # --------------------------------------------------
    # Select Destination containing GULF
    # --------------------------------------------------
    destination_select = Select(sb.find_element("#f_destination"))

    gulf_option = None

    print("\nAvailable Destinations:\n")

    for option in destination_select.options:

        text = option.text.strip()

        print(text)

        if "GULF" in text.upper():
            gulf_option = text

    if gulf_option is None:
        raise Exception("No destination containing GULF was found.")

    print(f"\nSelecting: {gulf_option}\n")

    destination_select.select_by_visible_text(gulf_option)

    # --------------------------------------------------
    # Wait for table to refresh
    # --------------------------------------------------
    sb.sleep(6)
    sb.wait_for_ready_state_complete()

    # --------------------------------------------------
    # Find all hyperlinks in the specification table
    # --------------------------------------------------
    print("\n" + "=" * 80)
    print("SPECIFICATION LINKS")
    print("=" * 80)

    links = sb.find_elements("css selector", "table a")

    print(f"Found {len(links)} links\n")

    unique_links = []

    seen = set()

    for i, link in enumerate(links, 1):

        text = link.text.strip()
        href = link.get_attribute("href")

        if not href:
            continue

        if href in seen:
            continue

        seen.add(href)

        unique_links.append(href)

        print(f"{len(unique_links)}.")
        print("TEXT :", text)
        print("LINK :", href)
        print("-" * 80)

    # --------------------------------------------------
    # Open first specification page
    # --------------------------------------------------
    if unique_links:

        print("\nOpening first specification page...\n")

        sb.uc_open_with_reconnect(unique_links[0], reconnect_time=5)

        try:
            sb.uc_gui_handle_captcha()
        except Exception:
            pass

        sb.wait_for_ready_state_complete()
        sb.sleep(3)

        print("=" * 80)
        print("CURRENT PAGE")
        print("=" * 80)
        print(sb.get_current_url())
        print(sb.get_title())

    else:

        print("\nNo hyperlinks found.")
        print("The table is probably using JavaScript click handlers instead of <a> tags.")

    input("\nPress ENTER to exit...")
