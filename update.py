import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re

def get_links():
    url = "https://t.me/s/happvpn"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    links = []
    for text in soup.find_all(text=re.compile(r'happ://crypt5/')):
        match = re.search(r'happ://crypt5/[A-Za-z0-9+/=]+', text)
        if match:
            links.append(match.group(0))
    return list(dict.fromkeys(links))[-4:]  # последние 4 уникальные

def decode_link(link):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        driver.get("https://happy-decoder.cc/")
        
        # Вставляем ссылку
        textarea = driver.find_element(By.TAG_NAME, "textarea")
        textarea.clear()
        textarea.send_keys(link)
        
        # Нажимаем "РАСШИФРОВАТЬ"
        button = driver.find_element(By.XPATH, "//button[contains(text(), 'РАСШИФРОВАТЬ')]")
        button.click()
        
        time.sleep(3)  # ждём расшифровки
        
        # Берём результат
        result = driver.find_element(By.CSS_SELECTOR, "pre, .result, textarea").text
        driver.quit()
        return result
    except Exception as e:
        return f"Ошибка декодирования: {str(e)}"

# Основная логика
links = get_links()
print(f"Найдено ссылок: {len(links)}")

with open("sobr.txt", "w", encoding="utf-8") as f:
    f.write(f"=== Обновление от {time.ctime()} ===\n")
    f.write(f"Найдено ссылок: {len(links)}\n\n")
    
    for link in links:
        f.write(f"🔓 {link}\n")
        decoded = decode_link(link)
        f.write(decoded + "\n")
        f.write("="*80 + "\n\n")

print("Готово!")
