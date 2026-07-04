import re
import time
from playwright.sync_api import sync_playwright

def get_crypt5_links():
    import requests
    resp = requests.get("https://t.me/s/happvpn", 
                       headers={"User-Agent": "Mozilla/5.0"})
    links = re.findall(r'happ://crypt5/[A-Za-z0-9+/=]+', resp.text)
    return list(dict.fromkeys(links))[-5:]

def decode_link(link):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto("https://happy-decoder.cc/", timeout=30000)
            
            # Вставляем ссылку
            page.fill("textarea", link)
            
            # Жмём кнопку
            page.click("button:has-text('РАСШИФРОВАТЬ')")
            
            # Ждём результат
            page.wait_for_timeout(5000)
            
            # Берём расшифрованный текст
            result = page.inner_text("pre, code, .result, textarea", timeout=10000)
            return result.strip()
        except Exception as e:
            return f"Ошибка расшифровки: {str(e)[:150]}"
        finally:
            browser.close()

# ===================== MAIN =====================
links = get_crypt5_links()

with open("sobr.txt", "w", encoding="utf-8") as f:
    f.write(f"=== HAPP VPN — Расшифрованные подписки ===\n")
    f.write(f"Обновлено: {time.ctime()} UTC\n")
    f.write(f"Ссылок обработано: {len(links)}\n\n")

    for i, link in enumerate(links, 1):
        f.write(f"[{i}] Исходная ссылка:\n{link}\n\n")
        print(f"Расшифровываю {i}/{len(links)}...")
        decoded = decode_link(link)
        f.write("РАСШИФРОВАНО:\n")
        f.write(decoded)
        f.write("\n\n" + "═"*90 + "\n\n")

print("Готово! Файл sobr.txt обновлён.")
