import requests
import re
import time
from bs4 import BeautifulSoup

def get_crypt5_links():
    url = "https://t.me/s/happvpn"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    links = re.findall(r'happ://crypt5/[A-Za-z0-9+/=]+', resp.text)
    return list(dict.fromkeys(links))[-4:]  # последние 4

def decode_link(link):
    try:
        # Прямой запрос к happy-decoder (если есть backend)
        data = {"input": link, "mode": "decrypt"}
        resp = requests.post("https://happy-decoder.cc/", data=data, timeout=10)
        
        if resp.status_code == 200:
            # Парсим результат со страницы
            soup = BeautifulSoup(resp.text, 'html.parser')
            result = soup.find(string=re.compile(r'https?://|vless://|vmess://'))
            if result:
                return result.strip()
            # Или весь большой блок
            pre = soup.find('pre')
            if pre:
                return pre.get_text()
    except:
        pass
    
    return "Не удалось расшифровать автоматически (сайт использует JS)"

# ======================
links = get_crypt5_links()

with open("sobr.txt", "w", encoding="utf-8") as f:
    f.write(f"=== Обновление подписок HAPP — {time.ctime()} ===\n\n")
    f.write(f"Найдено ссылок: {len(links)}\n\n")
    
    for i, link in enumerate(links, 1):
        f.write(f"Исходная: {link}\n\n")
        decoded = decode_link(link)
        f.write("РАСШИФРОВАНО:\n")
        f.write(decoded)
        f.write("\n\n" + "="*80 + "\n\n")

print("Обновлено! Проверь sobr.txt")
