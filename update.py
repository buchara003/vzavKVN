import os
import re
import base64
import requests

API_KEY = os.environ["HAPPY_API_KEY"]

# === ТОЛЬКО ОДИН КАНАЛ (как сейчас) ===
CHANNELS = {
    "happvpn": "https://t.me/s/happvpn"   # crypt5
}

API_URL = "https://happy-decoder.cc/api/v1/decrypt"

def get_last_links():
    print("Получаю Telegram канал happvpn...")
    html = requests.get(CHANNELS["happvpn"], timeout=20).text
    links = re.findall(r"happ://crypt5/[A-Za-z0-9+/=]+", html)
    unique = list(dict.fromkeys(links))
    print(f"Найдено {len(unique)} ссылок (берём последние 2)")
    return unique[-2:]


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
                decoded_subs.append(encoded)
        except Exception as e:
            print(f"❌ Ошибка для {link[:60]}...: {str(e)}")

    with open("sobr.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(encoded_subs))

    # Создаём sobr3.txt только с голыми протоколами из crypt4
    with open("sobr3.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(decoded_subs))

    with open("sobr2.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(encoded_subs))
        f.write("\n\n=== ОТ CRYPT4 (sobr3) ===\n")
        f.write("\n".join(decoded_subs))

    print(f"\n✅ Готово!")
    print(f"В sobr.txt  — только Base64 из happvpn")
    print(f"В sobr3.txt — голые протоколы из crypt4")
    print(f"В sobr2.txt — всё объединено")


if __name__ == "__main__":
    main() 
