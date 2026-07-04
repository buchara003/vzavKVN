import os
import re
import requests

API_KEY = os.environ["HAPPY_API_KEY"]

TELEGRAM_URL = "https://t.me/s/happvpn"

API_URL = "https://happy-decoder.cc/api/v1/decrypt"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}


def get_last_links():
    print("Получаю Telegram...")

    html = requests.get(TELEGRAM_URL, timeout=20).text

    links = re.findall(r"happ://crypt5/[A-Za-z0-9+/=]+", html)

    links = list(dict.fromkeys(links))

    if not links:
        raise Exception("Не найдено ни одного happ://crypt5")

    return links[-2:]


def decrypt(link):
    print("Расшифровываю...")

    r = requests.post(
        API_URL,
        headers=HEADERS,
        json={"url": link},
        timeout=20,
    )

    r.raise_for_status()

    data = r.json()

    if "error" in data:
        raise Exception(data["error"])

    return data["decryptedUrl"]


def download_subscription(url):
    print("Скачиваю подписку...")

    r = requests.get(url, timeout=30)

    r.raise_for_status()

    return r.text


def extract_configs(text):
    configs = []

    for line in text.splitlines():
        line = line.strip()

        if line.startswith((
            "vmess://",
            "vless://",
            "trojan://",
            "ss://",
            "ssr://",
            "tuic://",
            "hy2://",
            "hysteria://",
            "hysteria2://"
        )):
            configs.append(line)

    return configs


def main():

    all_configs = []

    links = get_last_links()

    print(f"Найдено {len(links)} crypt5")

    for link in links:

        try:
            sub_url = decrypt(link)

            print(sub_url)

            text = download_subscription(sub_url)

            configs = extract_configs(text)

            all_configs.extend(configs)

        except Exception as e:
            print(e)

    all_configs = list(dict.fromkeys(all_configs))

    with open("sobr.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_configs))

    print(f"Сохранено {len(all_configs)} конфигов")


if __name__ == "__main__":
    main()
