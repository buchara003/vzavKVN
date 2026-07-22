import os
import re
import base64
import requests

API_KEY = os.environ["HAPPY_API_KEY"]

CHANNELS = {
    "happvpn": "https://t.me/s/happvpn",   # crypt5
    "vpnruss1": "https://t.me/s/vpnruss1"  # crypt4
}

API_URL = "https://happy-decoder.cc/api/v1/decrypt"

def get_last_links():
    all_links = []
    for name, url in CHANNELS.items():
        print(f"Получаю {name}...")
        html = requests.get(url, timeout=20).text
        links = re.findall(r"happ://crypt[4-5]/[A-Za-z0-9+/=]+", html)
        unique = list(dict.fromkeys(links))
        all_links.extend(unique[-2:])
        print(f"В {name} найдено {len(unique)} (берём последние 2)")
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
                decoded_subs.append(encoded)
        except Exception as e:
            print(f"❌ Ошибка для {link[:60]}...: {str(e)}")

    with open("sobr.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(encoded_subs))

    # === САМЫЙ ВАЖНЫЙ БЛОК ===
    with open("sobr3.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(decoded_subs))

    with open("sobr2.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(encoded_subs))
        f.write("\n\n=== ОТ CRYPT4 (sobr3) ===\n")
        f.write("\n".join(decoded_subs))

    print(f"\n✅ Готово!")
    print(f"В sobr.txt  — {len(encoded_subs)} Base64")
    print(f"В sobr3.txt — {len(decoded_subs)} голые протоколы из crypt4")
    print(f"В sobr2.txt — всё объединено")


if __name__ == "__main__":
    main()
