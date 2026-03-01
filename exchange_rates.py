import requests
from datetime import datetime

# --- Investment details ---
INITIAL_ILS = 400_000.26       # ILS invested
PURCHASE_RATE = 3.078          # ILS per 1 USD at time of purchase
INITIAL_USD = INITIAL_ILS / PURCHASE_RATE  # USD purchased


def get_rates():
    # משיכת נתונים עבור USD, EUR, GBP מול ILS
    url = "https://api.frankfurter.dev/v1/latest?base=ILS&symbols=USD,EUR,GBP"
    response = requests.get(url)
    data = response.json()

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rates = data['rates']

    # חישוב השער ההפוך (כמה שקלים זה דולר אחד)
    usd_ils = round(1 / rates['USD'], 3)  # current ILS per USD
    eur_ils = round(1 / rates['EUR'], 3)
    gbp_ils = round(1 / rates['GBP'], 3)

    # --- Investment calculation ---
    current_ils_value = INITIAL_USD * usd_ils          # current ILS value of the USD held
    profit_ils = current_ils_value - INITIAL_ILS       # profit/loss in ILS
    profit_usd = profit_ils / usd_ils                  # profit/loss in USD
    pct_change = (profit_ils / INITIAL_ILS) * 100      # percentage change

    content = f"### עדכון שערים: {date_str}\n"
    content += f"- **USD/ILS**: {usd_ils}\n"
    content += f"- **EUR/ILS**: {eur_ils}\n"
    content += f"- **GBP/ILS**: {gbp_ils}\n\n"

    content += f"#### חישוב השקעה\n"
    content += f"- השקעה ראשונית: {INITIAL_ILS:,.2f} ILS בשער {PURCHASE_RATE} ILS/USD\n"
    content += f"- USD שנרכש: ${INITIAL_USD:,.2f}\n"
    content += f"- שווי נוכחי: {current_ils_value:,.2f} ILS (שער נוכחי: {usd_ils})\n"
    content += f"- רווח/הפסד: {profit_ils:+,.2f} ILS ({profit_usd:+,.2f} USD) | {pct_change:+.2f}%\n\n"

    # כתיבה לקובץ README.md (או log.md)
    with open("exchange_rates.md", "a") as f:
        f.write(content)


if __name__ == "__main__":
    get_rates()
