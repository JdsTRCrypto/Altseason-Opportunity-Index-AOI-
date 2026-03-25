import requests
import re
from datetime import datetime

TELEGRAM_TOKEN = ""   # será preenchido pelo secret
TELEGRAM_CHAT_ID = "" # será preenchido pelo secret

def get_fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=1", timeout=15)
        r.raise_for_status()
        data = r.json()['data'][0]
        print(f"Fear & Greed obtido: {data['value']}")
        return int(data['value'])
    except Exception as e:
        print(f"Erro ao buscar Fear & Greed: {e}")
        return None

def get_altcoin_season():
    try:
        r = requests.get("https://www.blockchaincenter.net/altcoin-season-index/", timeout=15)
        r.raise_for_status()
        text = r.text
        match = re.search(r'Altcoin Season \(?\s*(\d{1,3})\s*\)?', text, re.IGNORECASE)
        if not match:
            match = re.search(r'(\d{1,3})\s*(?:</|Altcoin)', text)
        if match:
            valor = int(match.group(1))
            if 0 <= valor <= 100:
                print(f"Altcoin Season Index obtido: {valor}")
                return valor
    except Exception as e:
        print(f"Erro ao buscar Altcoin Season: {e}")
    print("Não conseguiu pegar Altcoin Season")
    return None

def calcular():
    fng = get_fear_greed()
    alt = get_altcoin_season()
    
    if fng is None or alt is None:
        msg = "❌ Erro ao buscar os índices hoje. Verifique as APIs."
        print(msg)
        return msg
    
    resultado = (alt * 0.6) + ((100 - fng) * 0.4)
    
    if resultado >= 75:
        status = "🚀 FORTE SINAL DE ALTSEASON + OPORTUNIDADE"
    elif resultado >= 60:
        status = "✅ Bom momento para alts"
    elif resultado >= 45:
        status = "🟡 Neutro"
    elif resultado >= 30:
        status = "⚠️ Bitcoin dominando"
    else:
        status = "❌ Forte Bitcoin Season"
    
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M (BR)")
    
    msg = f"""📊 **Altseason Opportunity Index (AOI)**

Data: {data_atual}
Altcoin Season Index: **{alt}**
Fear & Greed Index: **{fng}**

**Resultado AOI:** **{resultado:.1f}**

{status}

Fórmula: (AltSeason × 0,6) + ((100 - F&G) × 0,4)
"""
    print("Cálculo realizado com sucesso!")
    return msg

def enviar_telegram(msg):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID não configurados nos Secrets!")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload, timeout=15)
        if r.status_code == 200:
            print("✅ Mensagem enviada com sucesso para o Telegram!")
        else:
            print(f"❌ Erro ao enviar Telegram: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ Exceção ao enviar Telegram: {e}")

if __name__ == "__main__":
    mensagem = calcular()
    enviar_telegram(mensagem)
