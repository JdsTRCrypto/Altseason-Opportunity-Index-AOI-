import requests
import json
from datetime import datetime

# ===================== CONFIGURAÇÕES =====================
TELEGRAM_TOKEN = "SEU_TOKEN_AQUI"          # Crie um bot no @BotFather
TELEGRAM_CHAT_ID = "SEU_CHAT_ID_AQUI"      # Seu ID no Telegram

# ===================== BUSCA DOS DADOS =====================
def get_fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=1")
        data = r.json()['data'][0]
        return int(data['value'])
    except:
        return None

def get_altcoin_season():
    # Blockchain Center (mais simples de scrapear)
    try:
        r = requests.get("https://www.blockchaincenter.net/altcoin-season-index/")
        text = r.text
        # Procura o número do índice (ex: "49" ou "53")
        import re
        match = re.search(r'(\d{1,3})\s*</', text)
        if match:
            return int(match.group(1))
    except:
        pass
    
    # Fallback: CoinGlass ou outros (pode ajustar)
    return None

# ===================== CÁLCULO =====================
def calcular():
    fng = get_fear_greed()
    alt = get_altcoin_season()
    
    if fng is None or alt is None:
        return "Erro ao buscar dados. Tente novamente mais tarde."
    
    resultado = (alt * 0.6) + ((100 - fng) * 0.4)
    
    # Interpretação
    if resultado >= 75:
        status = "🚀 FORTE SINAL DE ALTSEASON + OPORTUNIDADE (Medo + Altseason)"
    elif resultado >= 60:
        status = "✅ Bom momento para alts (Altseason moderada + algum medo)"
    elif resultado >= 45:
        status = "🟡 Neutro / Atenção"
    elif resultado >= 30:
        status = "⚠️ Bitcoin Season dominando"
    else:
        status = "❌ Forte Bitcoin Season – evite alts por enquanto"
    
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    mensagem = f"""📊 **Seu Cálculo Diário - Altseason Score**

Data: {data_atual}
Altcoin Season Index: **{alt}**
Fear & Greed Index: **{fng}**

**Resultado da fórmula:** **{resultado:.1f}**

{status}

Fórmula: (AltSeason × 0.6) + ((100 - F&G) × 0.4)
"""
    return mensagem

# ===================== ENVIO TELEGRAM =====================
def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
        print("✅ Alerta enviado com sucesso!")
    except:
        print("❌ Erro ao enviar Telegram")

# ===================== EXECUÇÃO =====================
if __name__ == "__main__":
    msg = calcular()
    print(msg)
    enviar_telegram(msg)
