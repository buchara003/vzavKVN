const https = require('https');
const fs = require('fs');

const API_KEY = "hd_demo_a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6";

async function fetchTelegram() {
  return new Promise((resolve) => {
    https.get('https://t.me/s/happvpn', (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });
  });
}

function extractLinks(html) {
  const regex = /happ:\/\/crypt5\/[A-Za-z0-9+/=]+/g;
  return [...new Set(html.match(regex) || [])].slice(-3); // последние 3
}

async function decodeLink(link) {
  const postData = JSON.stringify({ input: link });

  const options = {
    hostname: 'happy-decoder.cc',
    path: '/api',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY
    }
  };

  return new Promise((resolve) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.result || json.decoded || json);
        } catch(e) {
          resolve(data);
        }
      });
    });
    req.write(postData);
    req.end();
  });
}

async function main() {
  const html = await fetchTelegram();
  const links = extractLinks(html);

  let content = `=== HAPP VPN — Авто расшифровка ===\n`;
  content += `Обновлено: ${new Date().toUTCString()}\n\n`;

  for (let link of links) {
    content += `Исходная: ${link}\n\n`;
    console.log("Расшифровываю:", link.substring(0, 60) + "...");
    const result = await decodeLink(link);
    content += "РАСШИФРОВАНО:\n" + JSON.stringify(result, null, 2) + "\n\n";
    content += "─".repeat(90) + "\n\n";
  }

  fs.writeFileSync('sobr.txt', content);
  console.log("Готово!");
}

main().catch(console.error);
