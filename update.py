import requests
import re
import time

def get_last_two_crypt5():
    resp = requests.get(
        "https://t.me/s/happvpn",
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    
    # Находим все crypt5
    all_links = re.findall(r'happ://crypt5/[A-Za-z0-9+/=]+', resp.text)
    # Берём только последние 2 уникальные
    unique = list(dict.fromkeys(all_links))
    return unique[-2:]

def main():
    links = get_last_two_crypt5()
    
    with open("sobr.txt", "w", encoding="utf-8") as f:
        f.write("=== HAPP VPN — Последние 2 crypt5 ===\n")
        f.write(f"Обновлено: {time.ctime()} UTC\n\n")
        f.write("Как использовать:\n")
        f.write("1. Перейди → https://leeeet.dev/happ-decryptor/\n")
        f.write("2. Вставь ссылку ниже в поле\n")
        f.write("3. Нажми Decrypt\n")
        f.write("4. Скопируй результат (VLESS и т.д.)\n\n")
        f.write("═" * 80 + "\n\n")
        
        for i, link in enumerate(links, 1):
            f.write(f"[{i}] happ://crypt5 ссылка:\n{link}\n\n")
            f.write("─" * 60 + "\n\n")

    print(f"✅ Сохранено {len(links)} последних crypt5 ссылок.")

if __name__ == "__main__":
    main()
