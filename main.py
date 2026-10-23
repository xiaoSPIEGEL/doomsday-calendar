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

def process_commands(now):
    # Janela de tolerância (15 minutos antes ou depois)
    def in_window(target_hour, target_minute, window_mins=15):
        target = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
        diff = abs((now - target).total_seconds() / 60)
        return diff <= window_mins

    day_of_week = now.weekday()
    base_date = datetime.datetime(2026, 10, 5, tzinfo=datetime.timezone.utc)
    diff_cycle = (now.replace(hour=0, minute=0, second=0, microsecond=0) - base_date).days
    base_waste = datetime.datetime(2026, 10, 20, tzinfo=datetime.timezone.utc)
    diff_waste = (now.replace(hour=0, minute=0, second=0, microsecond=0) - base_waste).days

    # --- Fases do All-Star Night ---
    # 0=Seg (Aceleradores), 1=Ter (Heróis), 2=Qua (Treinamento), 3=Qui (Oficina), 4=Sex (Armamentos), 5=Sáb (Aceleradores), 6=Dom (Aceleradores)
    all_star_phase = diff_cycle % 14
    all_star_active = all_star_phase < 7
    
    # Dias em que a Maii pode ajudar com Buff
    buff_days = [0, 2, 5, 6] 
    
    # Eventos de hoje
    has_pompeii_today = (diff_cycle // 7) % 2 == 0 and day_of_week == 1
    has_off_limits_today = (diff_cycle // 7) % 2 != 0 and day_of_week == 1
    has_wasteland_today = (diff_waste % 14) in [0, 1, 2]
    
    # Eventos de amanhã
    tomorrow = day_of_week + 1 if day_of_week < 6 else 0
    tomorrow_week_num = ((now + datetime.timedelta(days=1)).day - 1) // 7 + 1
    is_pompeii_tomorrow = ((now + datetime.timedelta(days=1) - base_date).days // 7) % 2 == 0

    # ==========================================
    # TURNO DA MANHÃ (13:30 UTC)
    # ==========================================
    if in_window(13, 30):
        morning_msgs = []
        
        if day_of_week == 0:
            morning_msgs.append("⏰ *Get Ready!* *Anpede Hunt* starts soon (14:00 UTC). Gather your troops!")
        elif day_of_week == 1 and has_pompeii_today:
            morning_msgs.append("⏰ *Get Ready!* *The Recovery Of Pompeii* starts soon (15:00 UTC). Be on time!")
        elif day_of_week == 2:
            morning_msgs.append("⏰ *Get Ready!* *Horde Defense* starts soon (14:00 UTC). If you can't participate, check 'Offline Participation'.")
            
        if all_star_active and all_star_phase in buff_days:
            morning_msgs.append(f"👑 *{MAII_USERNAME} (R5)*: Today is an All-Star buff day! Don't forget the *Federation Buff* at 14:00 UTC!")
             
        if morning_msgs:
            send_telegram_message("\n\n".join(morning_msgs))

    # ==========================================
    # TURNO DA NOITE (23:00 UTC - Véspera e Fechamento)
    # ==========================================
    elif in_window(23, 0):
        evening_msgs = []
        
        # 1. Véspera (Amanhã)
        if tomorrow == 1:
            if is_pompeii_tomorrow:
                evening_msgs.append(f"📢 *Tomorrow:* The Recovery Of Pompeii!\n{REE_USERNAME} (R4), would you like to make an in-game reminder that there is still time for registrations?")
            else:
                evening_msgs.append("📢 *Tomorrow:* Off-Limits War! Start forming your teams of 8.")
            
            if (diff_waste + 1) % 14 == 0:
                evening_msgs.append("📢 *Tomorrow:* Wasteland Exploration! Form your teams of 4.")
                
        elif tomorrow == 2:
            if tomorrow_week_num == 2:
                evening_msgs.append(f"📢 *Tomorrow:* Archipelago Raid (AR)!\n{REE_USERNAME} (R4), would you like to remind everyone in-game to register?")
            elif tomorrow_week_num == 4:
                evening_msgs.append(f"📢 *Tomorrow:* Island Raid (IR)!\n{REE_USERNAME} (R4), would you like to remind everyone in-game to register?")
                 
        elif tomorrow == 4:
             if tomorrow_week_num == 4:
                 evening_msgs.append(f"📢 *Tomorrow:* Extreme Showdown!\n{REE_USERNAME} (R4), would you like to remind everyone in-game to register?")

        # 2. Fechamento do Dia / Domingo
        if day_of_week == 6: # Domingo
            evening_msgs.append("🪙 *Arena of Doom*: Don't forget to use your coins! They expire at reset.")
            evening_msgs.append("🔑 *District Showdown*: Time to use your keys on the enemy alliance vault. Check with R4/R5 which alliance to attack.")
        
        if all_star_active:
            evening_msgs.append("⭐ *All-Star Night*: Check the rank and decide if you'll invest resources to climb higher before reset!")
            
        if has_wasteland_today:
            evening_msgs.append("🏜️ *Wasteland*: Check the rank and decide whether to use Vigor flasks or save them for the next event.")
            
        # 3. Resumo Diário (Garante mínimo de 1 mensagem por dia)
        if not evening_msgs:
            if day_of_week == 0: evening_msgs.append("📅 *End of Day:* No major events ending today. A good time to farm and upgrade heroes! 🛡️")
            elif day_of_week == 3: evening_msgs.append("📅 *End of Day:* No major events ending today. Rest up, commanders! 🛡️")
            elif day_of_week == 5: evening_msgs.append("📅 *End of Day:* No major events ending today. Prepare for the weekend! 🛡️")
            else: evening_msgs.append("📅 *End of Day:* No events scheduled. A quiet day in the wasteland. 🛡️")

        if evening_msgs:
            send_telegram_message("\n\n".join(evening_msgs))

if __name__ == "__main__":
    now = datetime.datetime.now(datetime.timezone.utc)
    print(f"Rodando em: {now.strftime('%Y-%m-%d %H:%M')} UTC")
    process_commands(now)
