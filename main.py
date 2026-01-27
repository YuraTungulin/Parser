from playwright.sync_api import sync_playwright
import re
import time

RUS_CITIES = ["Москва", "Санкт-Петербург", "Краснодар", "Сочи", "Пятигорск"]
UKR_CITIES = ["Киев", "Днепр", "Черновцы", "Житомир"]
CITIES = RUS_CITIES + UKR_CITIES


def get_usdt_to_cash(page):
    rates = {}

    page.locator(".item", has_text="Ручной").click()
    page.wait_for_selector(".manual-variant", timeout=20000)
    page.locator(".manual-variant").first.click(force=True)
    time.sleep(1)

    for city in CITIES:
        page.click(".field-head-content")
        page.locator(".field-item-info span", has_text=city).first.click()
        time.sleep(0.5)

        if city in UKR_CITIES:
            block = page.locator(".exchanger-item.get").first
            block.locator(".field-coin-head-content").click()
            time.sleep(0.5)
            block.locator("._option_g1521_216", has_text="UAH").first.click()
            time.sleep(0.5)
            text = block.locator(".commission").inner_text()
        else:
            commission = page.locator(".commission")
            commission.wait_for(timeout=15000)
            text = commission.inner_text()

        match = re.search(r"≈\s*([\d,\.]+)", text)
        value = round(float(match.group(1).replace(",", ".")), 3) if match else 0

        rates[city] = value
        print(f"USDT→CASH | {city}: {value}")

    return rates


def get_cash_to_usdt(usdt_to_cash, page):
    rates = {}

    page.locator(".item", has_text="Ручной").click()
    page.wait_for_selector(".manual-variant", timeout=20000)

    variant = page.locator(".manual-variant", has_text="Наличные > Крипто").first
    variant.scroll_into_view_if_needed()
    variant.click(force=True)
    time.sleep(1)

    for city in CITIES:
        page.click(".field-head-content")
        page.locator(".field-item-info span", has_text=city).first.click()
        time.sleep(0.5)

        page.click(".field-coin-head-content")
        time.sleep(0.3)

        currency = "UAH" if city in UKR_CITIES else "RUB"
        page.locator("._option_g1521_216", has_text=currency).first.click()
        time.sleep(0.3)

        if city in UKR_CITIES:
            value = round(usdt_to_cash[city] * 1.022, 3)
        else:
            input_field = page.locator("input[placeholder='0.00']").first
            input_field.fill("1")
            time.sleep(0.8)

            error = page.locator(".error").inner_text()
            match = re.search(r"([\d\s\xa0,]+)\s*RUB", error)

            if match:
                raw = match.group(1).replace("\xa0", "").replace(" ", "").replace(",", ".")
                value = round(float(raw) / 1000, 3)
            else:
                value = "N/A"

        rates[city] = value
        print(f"CASH→USDT | {city}: {value}")

    return rates


def parse_rates():
    result = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()
        page.goto("https://URL.exchange/exchange", timeout=60000)
        page.wait_for_load_state("networkidle")
        usdt_to_cash = get_usdt_to_cash(page)
        result["USDT-CASH"] = usdt_to_cash
        page.close()

        page = browser.new_page()
        page.goto("https://URL.exchange/exchange", timeout=60000)
        page.wait_for_load_state("networkidle")
        result["CASH-USDT"] = get_cash_to_usdt(usdt_to_cash, page)
        page.close()

        browser.close()

    return result


if __name__ == "__main__":
    rates = parse_rates()
    print("\nRESULT:")
    print(rates)
