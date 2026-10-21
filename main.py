import os
import requests
import datetime

# Pega as credenciais que configuramos nos Segredos do GitHub
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Erro ao enviar mensagem: {response.text}")

def get_events_for_today():
    # Usa a data de HOJE em UTC
    now = datetime.datetime.now(datetime.timezone.utc)
    today_str = now.strftime("%Y-%m-%d")
    
    # Pega o dia da semana (0=Segunda, 1=Terça, ..., 6=Domingo)
    day_of_week = now.weekday()
    
    # Lista de eventos que começam hoje
    eventos = []
    
    # --- LÓGICA DOS EVENTOS (Baseada no nosso código do site) ---
    
    # SEGUNDA-FEIRA
    if day_of_week == 0:
        eventos.append("🌊 Water War")
        eventos.append("🏹 Anpede Hunt")
        # All-Star Night (a cada 14 dias)
        # A data base é 05/10/2026. Verifica se a diferença de dias é múltipla de 14.
        base_date = datetime.datetime(2026, 10, 5, tzinfo=datetime.timezone.utc)
        diff_days = (now.replace(hour=0, minute=0, second=0, microsecond=0) - base_date).days
        if diff_days >= 0 and diff_days % 14 == 0:
            eventos.append("⭐ All-Star Night")

    # TERÇA-FEIRA
    if day_of_week == 1:
        base_date_cycle = datetime.datetime(2026, 10, 5, tzinfo=datetime.timezone.utc)
        diff_days_cycle = (now.replace(hour=0, minute=0, second=0, microsecond=0) - base_date_cycle).days
        is_week1 = (diff_days_cycle // 7) % 2 == 0
        
        if is_week1:
            eventos.append("🏛️ The Recovery Of Pompeii")
        else:
            eventos.append("🚫 Off-Limits War")
            
        # Wasteland Exploration (a cada 14 dias a partir de 20/10/2026)
        base_date_waste = datetime.datetime(2026, 10, 20, tzinfo=datetime.timezone.utc)
        diff_days_waste = (now.replace(hour=0, minute=0, second=0, microsecond=0) - base_date_waste).days
        if diff_days_waste >= 0 and diff_days_waste % 14 == 0:
            eventos.append("🏜️ Wasteland Exploration")
            
        # Alliance League (Última terça do mês)
        next_week = now + datetime.timedelta(days=7)
        if now.month != next_week.month:
            eventos.append("🏆 Alliance League")

    # QUARTA-FEIRA
    if day_of_week == 2:
        eventos.append("🛡️ Horde Defense")
        
        # Archipelago Raid (2ª quarta) ou Island Raid (4ª quarta)
        week_number = (now.day - 1) // 7 + 1
        if week_number == 2:
            eventos.append("🏝️ Archipelago Raid (AR)")
        elif week_number == 4:
            eventos.append("🏝️ Island Raid (IR)")

    # SEXTA-FEIRA
    if day_of_week == 4:
        week_number = (now.day - 1) // 7 + 1
        if week_number == 2:
            eventos.append("⚔️ District Showdown")
        elif week_number == 4:
            eventos.append("💀 Extreme Showdown")

    return eventos

if __name__ == "__main__":
    print("Verificando eventos para hoje...")
    events = get_events_for_today()
    
    if events:
        message = "🚨 *Alliance Event Alert!* 🚨\n\n"
        message += "The following events are active today (UTC):\n\n"
        for ev in events:
            message += f"• {ev}\n"
        message += "\n_Get ready for the reset in 15 minutes!_ ⏳"
        
        print("Enviando mensagem para o Telegram...")
        send_telegram_message(message)
    else:
        print("Nenhum evento hoje. O Bot vai dormir.")
