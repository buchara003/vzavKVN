import os
import re
import base64
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
        raise Exception("Не найдено ни одной happ://crypt5 ссылки")

    print(f"Найдено {len(links)} ссылок")

    return links[-4:]


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

    print(f"Размер: {len(r.text)} символов")

    return r.text.strip()


def main():

    encoded_subs = []
    decoded_subs = []

    links = get_last_links()

    for link in links:
        try:
            sub_url = decrypt(link)

            encoded = download(sub_url)

            encoded_subs.append(encoded)

            try:
                decoded = base64.b64decode(encoded).decode(
                    "utf-8",
                    errors="ignore"
                )

                decoded_subs.append(decoded)

                print("Подписка успешно декодирована")

            except Exception as e:
                print("Ошибка декодирования:", e)

        except Exception as e:
            print("Ошибка:", e)

    with open("sobr.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(encoded_subs))

    with open("sobr2.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(decoded_subs))

    print("Готово.")
    print(f"Сохранено Base64 подписок: {len(encoded_subs)}")
    print(f"Сохранено декодированных подписок: {len(decoded_subs)}")


if __name__ == "__main__":
    main()
