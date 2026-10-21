import os
import requests
import datetime

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
REE_USERNAME = os.environ.get("REE_USERNAME", "@ReePatr1cia") 
MAII_USERNAME = os.environ.get("MAII_USERNAME", "@Mayo017")   

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Erro ao enviar mensagem: {response.text}")

def get_daily_events_info(now):
    day_of_week = now.weekday()
    eventos = []

    # --- Event Logic (Current Day) ---
    if day_of_week == 0: # Monday
        eventos.append("🏹 Anpede Hunt (14:00 UTC)")
        if (now - datetime.datetime(2026, 10, 5, tzinfo=datetime.timezone.utc)).days % 14 == 0:
            eventos.append("⭐ All-Star Night")
    elif day_of_week == 1: # Tuesday
        if ((now - datetime.datetime(2026, 10, 5, tzinfo=datetime.timezone.utc)).days // 7) % 2 == 0:
            eventos.append("🏛️ The Recovery Of Pompeii (15:00 UTC)")
        else:
            eventos.append("🚫 Off-Limits War")
        if (now - datetime.datetime(2026, 10, 20, tzinfo=datetime.timezone.utc)).days % 14 == 0:
            eventos.append("🏜️ Wasteland Exploration")
    elif day_of_week == 2: # Wednesday
        eventos.append("🛡️ Horde Defense (14:00 UTC)")
    elif day_of_week == 4: # Friday
        week_num = (now.day - 1) // 7 + 1
        if week_num == 2: eventos.append("⚔️ District Showdown")
        elif week_num == 4: eventos.append("💀 Extreme Showdown")

    return eventos

def process_commands(now):
    hour = now.hour
    minute = now.minute
    day_of_week = now.weekday() # 0=Mon, 6=Sun
    events_today = get_daily_events_info(now)
    
    # --- 13:30 UTC (Preparation for Events) ---
    if hour == 13 and minute == 30:
        msg = ""
        if day_of_week == 0:
            msg = "⏰ *Get Ready!* *Anpede Hunt* starts in 30 minutes (14:00 UTC). Gather your troops and find a safe spot!"
        elif day_of_week == 2:
            msg = "⏰ *Get Ready!* *Horde Defense* starts in 30 minutes (14:00 UTC). If you can't participate actively, don't forget to check the 'Offline Participation' box."
        elif day_of_week == 1 and "The Recovery Of Pompeii" in " ".join(events_today):
            msg = "⏰ *Get Ready!* *The Recovery Of Pompeii* starts in 30 minutes (15:00 UTC). It's an important GvG event, be on time!"
            
        if "All-Star Night" in " ".join(events_today):
             # CORRIGIDO: f-string unificada
             msg += f"\n\n👑 *{MAII_USERNAME} (R5)*: Don't forget the *Federation Buff* at 14:00 UTC!"
             
        if msg: send_telegram_message(msg)
        
    # --- 23:00 UTC (Eve Reminders - 1 hour before reset) ---
    elif hour == 23 and minute == 0:
        full_msg = []
        
        tomorrow = day_of_week + 1 if day_of_week < 6 else 0
        tomorrow_week_num = (now.day + 1 - 1) // 7 + 1 
        
        if tomorrow == 1: # Tuesday
            # Pompeii Check
            if ((now - datetime.datetime(2026, 10, 5, tzinfo=datetime.timezone.utc)).days + 1) // 7 % 2 == 0:
                 # CORRIGIDO: f-string unificada
                 full_msg.append(f"📢 *Tomorrow:* The Recovery Of Pompeii!\n{REE_USERNAME} (R4), would you like to make an in-game reminder that there is still time for registrations?")
            # Off-Limits Check
            else:
                 full_msg.append("📢 *Tomorrow:* Off-Limits War! Start forming your teams of 8.")
                 
            # Wasteland Check
            if ((now - datetime.datetime(2026, 10, 20, tzinfo=datetime.timezone.utc)).days + 1) % 14 == 0:
                 full_msg.append("📢 *Tomorrow:* Wasteland Exploration! Form your teams of 4.")
                 
        elif tomorrow == 2: # Wednesday (AR / IR)
            if tomorrow_week_num == 2:
                 # CORRIGIDO: f-string unificada
                 full_msg.append(f"📢 *Tomorrow:* Archipelago Raid (AR)!\n{REE_USERNAME} (R4), would you like to remind everyone in-game to register?")
            elif tomorrow_week_num == 4:
                 # CORRIGIDO: f-string unificada
                 full_msg.append(f"📢 *Tomorrow:* Island Raid (IR)!\n{REE_USERNAME} (R4), would you like to remind everyone in-game to register?")
                 
        elif tomorrow == 4: # Friday (Extreme Showdown)
             if tomorrow_week_num == 4:
                 # CORRIGIDO: f-string unificada
                 full_msg.append(f"📢 *Tomorrow:* Extreme Showdown!\n{REE_USERNAME} (R4), would you like to remind everyone in-game to register?")

        if full_msg:
            send_telegram_message("\n\n".join(full_msg))

    # --- 23:30 UTC (Closing Events & Sundays) ---
    elif hour == 23 and minute == 30:
        msgs = []
        if day_of_week == 6: # Sunday
            msgs.append("🪙 *Arena of Doom*: Don't forget to use your coins! They expire at reset.")
            msgs.append("🔑 *District Showdown*: Time to use your keys on the enemy alliance vault. Check with R4/R5 which alliance to attack.")
        
        if "All-Star Night" in " ".join(events_today):
            msgs.append("⭐ *All-Star Night*: Check the rank and decide if you'll invest resources to climb higher before reset!")
            
        if "Wasteland Exploration" in " ".join(events_today):
            msgs.append("🏜️ *Wasteland*: Check the rank and decide whether to use Vigor flasks or save them for the next event.")
            
        if msgs:
            send_telegram_message("\n\n".join(msgs))

if __name__ == "__main__":
    # =====================================================
    # TESTE FORÇADO: Duas mensagens separadas (inglês)
    # =====================================================
    # print("Iniciando testes...")
    # 
    # msg_teste_ree = f"🧪 *TEST 1 - Pompeii Reminder:*\n📢 *Tomorrow:* The Recovery Of Pompeii!\n{REE_USERNAME} (R4), would you like to make an in-game reminder that there is still time for registrations?"
    # send_telegram_message(msg_teste_ree)
    # 
    # msg_teste_maii = f"🧪 *TEST 2 - Federation Buff:*\n👑 *{MAII_USERNAME} (R5)*: Don't forget the *Federation Buff* at 14:00 UTC!"
    # send_telegram_message(msg_teste_maii)
    # 
    # print("Testes enviados!")
    
    # --- PRODUÇÃO ---
    now = datetime.datetime.now(datetime.timezone.utc)
    print(f"Rodando em: {now.strftime('%Y-%m-%d %H:%M')} UTC")
    process_commands(now)
