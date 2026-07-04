import os
import re
import requests

API_KEY = os.environ["HAPPY_API_KEY"]

TELEGRAM_URL = "https://t.me/s/happvpn"
API_URL = "https://happy-decoder.cc/api/v1/decrypt"


def get_last_links():
    print("Получаю Telegram...")

    html = requests.get(TELEGRAM_URL, timeout=20).text

    links = re.findall(r"happ://crypt5/[A-Za-z0-9+/=]+", html)

    links = list(dict.fromkeys(links))

    if not links:
        raise Exception("Не найдено ни одного happ://crypt5")

    print(f"Найдено {len(links)} ссылок")

    return links[-3:]


def decrypt(link):
    print("Расшифровываю:")
    print(link[:80] + "...")

    r = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}"
        },
        json={
            "url": link
        },
        timeout=20,
    )

    r.raise_for_status()

    data = r.json()

    if "error" in data:
        raise Exception(data["error"])

    return data["decryptedUrl"]


def download(url):
    print("Скачиваю подписку...")
    print(url)

    r = requests.get(url, timeout=30)

    r.raise_for_status()

    print("Размер:", len(r.text), "символов")

    return r.text


def main():

    result = []

    links = get_last_links()

    for link in links:

        try:

            sub = decrypt(link)

            text = download(sub)

            result.append(text)

        except Exception as e:
            print("Ошибка:", e)

    with open("sobr.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(result))

    print("Готово.")


if __name__ == "__main__":
    main()
