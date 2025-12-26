from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json


def handle(data):
    try:
        banks_data = parse_minfin_currency()

        # Add parsed data to the response
        data['currency_rates'] = banks_data
        data['status'] = 'success'
        data['total_banks'] = len(banks_data)

        return data

    except Exception as e:
        data['status'] = 'error'
        data['error_message'] = str(e)
        return data


def parse_minfin_currency():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)

    try:
        url = "https://minfin.com.ua/ua/currency/"
        driver.get(url)
        print(f"Завантажено: {url}")
        time.sleep(5)

        # Знаходимо всі таблиці
        tables = driver.find_elements(By.TAG_NAME, "table")
        print(f"Знайдено таблиць: {len(tables)}")

        # Беремо 3-ю таблицю (індекс 2)
        if len(tables) >= 3:
            table = tables[2]
            rows = table.find_elements(By.TAG_NAME, "tr")

            banks_data = []

            # Пропускаємо перші 2 рядки (заголовки)
            for row in rows[2:]:
                cols = row.find_elements(By.TAG_NAME, "td")

                if len(cols) >= 4:
                    bank_name = cols[0].text.strip()
                    cash = cols[1].text.strip()  # В касах банків
                    card = cols[2].text.strip()  # При оплаті карткою
                    updated = cols[3].text.strip()  # Час оновлення

                    # Парсимо курси по картках
                    if card and card != '- / -':
                        parts = card.split(' / ')
                        if len(parts) == 2:
                            bank = {
                                'bank': bank_name,
                                'buy': parts[0].strip(),
                                'sell': parts[1].strip(),
                                'updated': updated
                            }
                            banks_data.append(bank)

            return banks_data
        else:
            return []

    finally:
        driver.quit()


if __name__ == "__main__":
    test_data = {}
    result = handle(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))