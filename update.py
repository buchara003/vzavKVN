import os
import re
import requests
from datetime import datetime

API_KEY = os.environ["HAPPY_API_KEY"]

# === КАНАЛЫ ===
CHANNELS = {
    "happvpn": "https://t.me/s/happvpn",
    "vpnruss1": "https://t.me/s/vpnruss1"
}

API_URL = "https://happy-decoder.cc/api/v1/decrypt"

def get_last_links():
    all_links = []
    for name, url in CHANNELS.items():
        print(f"Получаю Telegram канал: {name}")
        html = requests.get(url, timeout=20).text
        links = re.findall(r"happ://crypt[4-5]/[A-Za-z0-9+/=]+", html)
        unique = list(dict.fromkeys(links))
        all_links.extend(unique[-2:])  # по 2 из каждого канала
        print(f"Найдено в {name}: {len(unique)} ссылок (берём последние 2)")

    if not all_links:
        raise Exception("Не найдено ни одной happ://crypt ссылок")

    return all_links


def decrypt(link):
    print(f"Расшифровываю: {link[:80]}...")
    r = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"url": link},
        timeout=20,
    )
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise Exception(data["error"])
    return data.get("decryptedUrl") or data.get("result")


def download(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text.strip()


def main():
    links = get_last_links()
    encoded_subs = []
    decoded_subs = []

    for link in links:
        try:
            sub_url = decrypt(link)
            encoded = download(sub_url)
            encoded_subs.append(encoded)

            try:
                decoded = base64.b64decode(encoded).decode("utf-8", errors="ignore")
                decoded_subs.append(decoded)
            except:
                pass
        except Exception as e:
            print(f"Ошибка для {link[:60]}...: {e}")

    with open("sobr.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(encoded_subs))
    with open("sobr2.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(decoded_subs))

    print(f"\n✅ Готово!")
    print(f"Сохранено Base64 подписок: {len(encoded_subs)}")
    print(f"Сохранено декодированных подписок: {len(decoded_subs)}")


if __name__ == "__main__":
    main()
