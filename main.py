import os
import requests
import datetime

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Erro ao enviar mensagem: {response.text}")

def get_daily_events_info(now):
    day_of_week = now.weekday()
    eventos = []
    avisos_especiais = []

    # --- Lógica de Eventos (Dia Atual) ---
    if day_of_week == 0: # Segunda
        eventos.append("🏹 Anpede Hunt (14:00 UTC)")
        if (now - datetime.datetime(2026, 10, 5, tzinfo=datetime.timezone.utc)).days % 14 == 0:
            eventos.append("⭐ All-Star Night")
    elif day_of_week == 1: # Terça
        if ((now - datetime.datetime(2026, 10, 5, tzinfo=datetime.timezone.utc)).days // 7) % 2 == 0:
            eventos.append("🏛️ The Recovery Of Pompeii (15:00 UTC)")
        else:
            eventos.append("🚫 Off-Limits War")
        if (now - datetime.datetime(2026, 10, 20, tzinfo=datetime.timezone.utc)).days % 14 == 0:
            eventos.append("🏜️ Wasteland Exploration")
    elif day_of_week == 2: # Quarta
        eventos.append("🛡️ Horde Defense (14:00 UTC)")
    elif day_of_week == 4: # Sexta
        week_num = (now.day - 1) // 7 + 1
        if week_num == 2: eventos.append("⚔️ District Showdown")
        elif week_num == 4: eventos.append("💀 Extreme Showdown")

    return eventos

def process_commands(now):
    hour = now.hour
    minute = now.minute
    day_of_week = now.weekday() # 0=Seg, 6=Dom
    events_today = get_daily_events_info(now)
    
    # --- 13:30 UTC (Preparação para Eventos) ---
    if hour == 13 and minute == 30:
        msg = ""
        if day_of_week == 0:
            msg = "⏰ *Prepare-se!* O *Anpede Hunt* começa em 30 minutos (14:00 UTC). Recolha suas tropas e encontre um local seguro!"
        elif day_of_week == 2:
            msg = "⏰ *Prepare-se!* O *Horde Defense* começa em 30 minutos (14:00 UTC). Se não puder participar ativamente, não esqueça de marcar a caixinha de 'Participação Offline'."
        elif day_of_week == 1 and "The Recovery Of Pompeii" in " ".join(events_today):
            msg = "⏰ *Prepare-se!* O *The Recovery Of Pompeii* começa em 30 minutos (15:00 UTC). É um GvG importante, seja pontual!"
            
        # Lembrete para a Witch (All-Star Night)
        if "All-Star Night" in " ".join(events_today):
             msg += "\n\n👑 *Witch (R5)*: Não esqueça do *Federation Buff* às 14:00 UTC!"
             
        if msg: send_telegram_message(msg)
        
    # --- 23:30 UTC (Fechamentos e Domingos) ---
    elif hour == 23 and minute == 30:
        msgs = []
        if day_of_week == 6: # Domingo
            msgs.append("🪙 *Arena of Doom*: Não esqueça de usar suas moedas! Elas expiram no reset.")
            msgs.append("🔑 *District Showdown*: Hora de usar as chaves no cofre da aliança inimiga. Verifique com a R4/R5 qual aliança atacar.")
        
        if "All-Star Night" in " ".join(events_today):
            msgs.append("⭐ *All-Star Night*: Verifique o rank e decida se investirá recursos para subir de posição antes do reset!")
            
        if "Wasteland Exploration" in " ".join(events_today):
            msgs.append("🏜️ *Wasteland*: Verifique o rank e decida se usará frascos de Vigor ou guardará para o próximo evento.")
            
        if msgs:
            send_telegram_message("\n\n".join(msgs))

    # --- 23:45 UTC (Resumo Diário e Vésperas) ---
    elif hour == 23 and minute == 45:
        full_msg = []
        
        # 1. Avisos de Véspera (Amanhã)
        tomorrow = day_of_week + 1 if day_of_week < 6 else 0
        if tomorrow == 1:
            if ((now - datetime.datetime(2026, 10, 5, tzinfo=datetime.timezone.utc)).days + 1) // 7 % 2 == 0:
                 full_msg.append("📢 *Amanhã:* The Recovery Of Pompeii! Falem com a *Ree (R4)* para fazer a inscrição. Participação é crucial!")
            else:
                 full_msg.append("📢 *Amanhã:* Off-Limits War! Comecem a formar seus times de 8 pessoas.")
            if ((now - datetime.datetime(2026, 10, 20, tzinfo=datetime.timezone.utc)).days + 1) % 14 == 0:
                 full_msg.append("📢 *Amanhã:* Wasteland Exploration! Formem seus times de 4 pessoas.")

        # 2. Resumo do dia de hoje
        if events_today:
            digest = "📅 *Resumo de Hoje (UTC):*\n" + "\n".join([f"• {ev}" for ev in events_today])
            full_msg.append(digest)
            
        if full_msg:
            send_telegram_message("\n\n".join(full_msg))

if __name__ == "__main__":
    now = datetime.datetime.now(datetime.timezone.utc)
    print(f"Rodando em: {now.strftime('%Y-%m-%d %H:%M')} UTC")
    process_commands(now)
