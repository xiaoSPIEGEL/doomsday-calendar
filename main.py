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

def get_active_events(now):
    day_of_week = now.weekday()
    eventos = []
    
    base_cycle = datetime.datetime(2026, 10, 5, tzinfo=datetime.timezone.utc)
    base_waste = datetime.datetime(2026, 10, 20, tzinfo=datetime.timezone.utc)
    
    diff_cycle = (now.replace(hour=0, minute=0, second=0, microsecond=0) - base_cycle).days
    diff_waste = (now.replace(hour=0, minute=0, second=0, microsecond=0) - base_waste).days

    if diff_waste >= 0 and (diff_waste % 14) in [0, 1, 2]:
        eventos.append("🏜️ Wasteland Exploration")
    if diff_cycle >= 0 and (diff_cycle % 14) < 7:
        eventos.append("⭐ All-Star Night")

    next_week = now + datetime.timedelta(days=7)
    if day_of_week == 1 and now.month != next_week.month:
        eventos.append("🏆 Alliance League")
    elif day_of_week in [2, 3, 4, 5, 6]:
        last_tuesday = now - datetime.timedelta(days=(day_of_week - 1))
        if last_tuesday.month != (last_tuesday + datetime.timedelta(days=7)).month:
            if (now - last_tuesday).days < 6:
                eventos.append("🏆 Alliance League")

    if day_of_week == 0:
        eventos.append("🏹 Anpede Hunt (14:00 UTC)")
    elif day_of_week == 1:
        if (diff_cycle // 7) % 2 == 0:
            eventos.append("🏛️ The Recovery Of Pompeii (15:00 UTC)")
        else:
            eventos.append("🚫 Off-Limits War")
    elif day_of_week == 2:
        eventos.append("🛡️ Horde Defense (14:00 UTC)")
        
    week_num = (now.day - 1) // 7 + 1
    if day_of_week == 2:
        if week_num == 2: eventos.append("🏝️ Archipelago Raid (AR)")
        elif week_num == 4: eventos.append("🏝️ Island Raid (IR)")
    elif day_of_week in [3, 4, 5, 6]:
        start_of_week = now - datetime.timedelta(days=(day_of_week - 2))
        start_week_num = (start_of_week.day - 1) // 7 + 1
        if start_week_num == 2: eventos.append("🏝️ Archipelago Raid (AR)")
        elif start_week_num == 4: eventos.append("🏝️ Island Raid (IR)")

    if day_of_week == 4:
        if week_num == 2: eventos.append("⚔️ District Showdown")
        elif week_num == 4: eventos.append("💀 Extreme Showdown")
    elif day_of_week in [5, 6]:
        start_of_week = now - datetime.timedelta(days=(day_of_week - 4))
        start_week_num = (start_of_week.day - 1) // 7 + 1
        if start_week_num == 2: eventos.append("⚔️ District Showdown")
        elif start_week_num == 4: eventos.append("💀 Extreme Showdown")

    return list(set(eventos))

def process_commands(now):
    # A MÁGICA DA JANELA DE TEMPO (Tolerância de 15 minutos para mais ou para menos)
    def in_window(target_hour, target_minute, window_mins=15):
        target = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
        diff = abs((now - target).total_seconds() / 60)
        return diff <= window_mins

    day_of_week = now.weekday()
    events_today = get_active_events(now)
    
    # --- 13:30 UTC (Preparação) - Janela de 13:15 a 13:45 ---
    if in_window(13, 30):
        msg = ""
        if day_of_week == 0:
            msg = "⏰ *Get Ready!* *Anpede Hunt* starts soon (14:00 UTC). Gather your troops and find a safe spot!"
        elif day_of_week == 2:
            msg = "⏰ *Get Ready!* *Horde Defense* starts soon (14:00 UTC). If you can't participate actively, don't forget to check the 'Offline Participation' box."
        elif day_of_week == 1 and "The Recovery Of Pompeii" in " ".join(events_today):
            msg = "⏰ *Get Ready!* *The Recovery Of Pompeii* starts soon (15:00 UTC). It's an important GvG event, be on time!"
            
        if "All-Star Night" in " ".join(events_today):
             msg += f"\n\n👑 *{MAII_USERNAME} (R5)*: Don't forget the *Federation Buff* at 14:00 UTC!"
             
        if msg: send_telegram_message(msg)
        
    # --- 23:00 UTC (Véspera) - Janela de 22:45 a 23:15 ---
    elif in_window(23, 0):
        full_msg = []
        tomorrow = day_of_week + 1 if day_of_week < 6 else 0
        tomorrow_week_num = (now.day + 1 - 1) // 7 + 1 
        
        if tomorrow == 1:
            if ((now - datetime.datetime(2026, 10, 5, tzinfo=datetime.timezone.utc)).days + 1) // 7 % 2 == 0:
                 full_msg.append(f"📢 *Tomorrow:* The Recovery Of Pompeii!\n{REE_USERNAME} (R4), would you like to make an in-game reminder that there is still time for registrations?")
            else:
                 full_msg.append("📢 *Tomorrow:* Off-Limits War! Start forming your teams of 8.")
            if ((now - datetime.datetime(2026, 10, 20, tzinfo=datetime.timezone.utc)).days + 1) % 14 == 0:
                 full_msg.append("📢 *Tomorrow:* Wasteland Exploration! Form your teams of 4.")
                 
        elif tomorrow == 2:
            if tomorrow_week_num == 2:
                 full_msg.append(f"📢 *Tomorrow:* Archipelago Raid (AR)!\n{REE_USERNAME} (R4), would you like to remind everyone in-game to register?")
            elif tomorrow_week_num == 4:
                 full_msg.append(f"📢 *Tomorrow:* Island Raid (IR)!\n{REE_USERNAME} (R4), would you like to remind everyone in-game to register?")
                 
        elif tomorrow == 4:
             if tomorrow_week_num == 4:
                 full_msg.append(f"📢 *Tomorrow:* Extreme Showdown!\n{REE_USERNAME} (R4), would you like to remind everyone in-game to register?")

        if full_msg: send_telegram_message("\n\n".join(full_msg))

    # --- 23:30 UTC (Fechamento e Domingos) - Janela de 23:15 a 23:45 ---
    elif in_window(23, 30):
        msgs = []
        if day_of_week == 6: # Sunday
            msgs.append("🪙 *Arena of Doom*: Don't forget to use your coins! They expire at reset.")
            msgs.append("🔑 *District Showdown*: Time to use your keys on the enemy alliance vault. Check with R4/R5 which alliance to attack.")
        
        if "All-Star Night" in " ".join(events_today):
            msgs.append("⭐ *All-Star Night*: Check the rank and decide if you'll invest resources to climb higher before reset!")
        if "Wasteland Exploration" in " ".join(events_today):
            msgs.append("🏜️ *Wasteland*: Check the rank and decide whether to use Vigor flasks or save them for the next event.")
            
        if msgs: send_telegram_message("\n\n".join(msgs))

    # --- 23:45 UTC (Resumo Diário) - Janela de 23:30 a 00:00 ---
    elif in_window(23, 45, window_mins=15):
        if events_today:
            digest = "📅 *Today's Event Summary (UTC):*\n" + "\n".join([f"• {ev}" for ev in events_today])
            digest += "\n\n_Good luck and have fun!_ ⚔️"
            send_telegram_message(digest)
        else:
            send_telegram_message("📅 *Today's Event Summary:*\nNo major events scheduled for today. A good day to rest, farm, and upgrade your heroes! 🛡️")

if __name__ == "__main__":
    # TESTE FORÇADO
    # now = datetime.datetime.now(datetime.timezone.utc).replace(hour=23, minute=40)
    # print(f"Rodando TESTE em: {now.strftime('%Y-%m-%d %H:%M')} UTC")
    # process_commands(now)
    
    # PRODUÇÃO
    now = datetime.datetime.now(datetime.timezone.utc)
    print(f"Rodando em: {now.strftime('%Y-%m-%d %H:%M')} UTC")
    process_commands(now)
