import requests
from datetime import datetime

def get_rates():
    # משיכת נתונים עבור USD, EUR, GBP מול ILS
    url = "https://api.frankfurter.dev/v1/latest?base=ILS&symbols=USD,EUR,GBP"
    response = requests.get(url)
    data = response.json()

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rates = data['rates']

    # חישוב השער ההפוך (כמה שקלים זה דולר אחד)
    content = f"### עדכון שערים: {date_str}\n"
    content += f"- **USD/ILS**: {round(1/rates['USD'], 3)}\n"
    content += f"- **EUR/ILS**: {round(1/rates['EUR'], 3)}\n"
    content += f"- **GBP/ILS**: {round(1/rates['GBP'], 3)}\n\n"

    # כתיבה לקובץ README.md (או log.md)
    with open("exchange_rates.md", "a") as f:
        f.write(content)

if __name__ == "__main__":
    get_rates()
