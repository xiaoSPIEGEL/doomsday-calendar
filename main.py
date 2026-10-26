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
    # Janela de tolerância flexível (30 minutos para os dois turnos)
    def in_window(target_hour, target_minute, window_mins=30):
        target = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
        diff = abs((now - target).total_seconds() / 60)
        return diff <= window_mins

    day_of_week = now.weekday()
    base_date = datetime.datetime(2026, 10, 5, tzinfo=datetime.timezone.utc)
    diff_cycle = (now.replace(hour=0, minute=0, second=0, microsecond=0) - base_date).days
    base_waste = datetime.datetime(2026, 10, 20, tzinfo=datetime.timezone.utc)
    diff_waste = (now.replace(hour=0, minute=0, second=0, microsecond=0) - base_waste).days

    # --- Fases do All-Star Night ---
    all_star_phase = diff_cycle % 14
    all_star_active = all_star_phase < 7
    buff_days = [0, 2, 5, 6] 
    
    # --- Eventos de Hoje ---
    has_pompeii_today = (diff_cycle // 7) % 2 == 0 and day_of_week == 1
    has_wasteland_today = (diff_waste % 14) in [0, 1, 2]
    is_last_week_of_month = (now.day + 7) > 28 # Verifica se está na última semana
    
    current_week_num = (now.day - 1) // 7 + 1

    # --- Eventos de Amanhã ---
    tomorrow = day_of_week + 1 if day_of_week < 6 else 0
    tomorrow_date = now + datetime.timedelta(days=1)
    tomorrow_week_num = (tomorrow_date.day - 1) // 7 + 1
    is_pompeii_tomorrow = ((tomorrow_date - base_date).days // 7) % 2 == 0

    # ==========================================
    # TURNO DA MANHÃ (12:00 UTC)
    # ==========================================
    if in_window(12, 0):
        morning_msgs = []
        
        # Ações do dia (Hoje)
        if day_of_week == 0:
            morning_msgs.append("⏰ *Get Ready!* *Anpede Hunt* starts soon (14:00 UTC). Gather your troops!")
        elif day_of_week == 1 and has_pompeii_today:
            morning_msgs.append("⏰ *Get Ready!* *The Recovery Of Pompeii* starts soon (15:00 UTC). It's an important event, be on time!")
        elif day_of_week == 2:
            morning_msgs.append("⏰ *Get Ready!* *Horde Defense* starts soon (14:00 UTC). If you can't participate, check 'Offline Participation'.")
        elif day_of_week == 3 and is_last_week_of_month:
            morning_msgs.append("⏰ *Get Ready!* *Back Alley Doctor's Request* bosses start soon (15:00 UTC). Log in 15 minutes early, gather your squads, and get ready when R4/R5 summons the bosses!")
            
        # Lembrete da Maii
        if all_star_active and all_star_phase in buff_days:
            morning_msgs.append(f"👑 *{MAII_USERNAME} (R5)*: Today is an All-Star buff day! Don't forget the *Federation Buff* at 14:00 UTC!")
             
        if morning_msgs:
            send_telegram_message("\n\n".join(morning_msgs))

    # ==========================================
    # TURNO DA NOITE (23:00 UTC)
    # ==========================================
    elif in_window(23, 0):
        evening_msgs = []
        
        # --- PARTE 1: Avisos de Véspera (Amanhã) ---
        if tomorrow == 0: # Amanhã é Segunda
            evening_msgs.append("📢 *Tomorrow:* *Biohazard Frenzy* starts! Complete missions as fast as possible. Points are cumulative, so the earlier you rank up, the easier it is to keep a good position!")
            evening_msgs.append("📢 *Tomorrow:* *Flash Sales*! Set your alarms: 01:00 UTC, 09:00 UTC, and 17:00 UTC for 30 General Speedups (60m each) for 1000 diamonds? Don't miss it!")
            if is_last_week_of_month:
                evening_msgs.append("📢 *Tomorrow:* *Back Alley Doctor's Request* starts! Great rewards, low effort. Individual efforts add up to better prizes. Don't leave individual missions for the last day!")
                
        elif tomorrow == 1: # Amanhã é Terça
            if is_pompeii_tomorrow:
                evening_msgs.append(f"📢 *Tomorrow:* *The Recovery Of Pompeii*!\n{REE_USERNAME} (R4), would you like to make an in-game reminder that there is still time for registrations?")
            else:
                evening_msgs.append("📢 *Tomorrow:* *Off-Limits War*! Start forming your teams of 8.")
            
            if (diff_waste + 1) % 14 == 0:
                evening_msgs.append("📢 *Tomorrow:* *Wasteland Exploration*! Start forming your teams of 4.")
                
        elif tomorrow == 2: # Amanhã é Quarta
            if tomorrow_week_num == 2:
                evening_msgs.append("📢 *Tomorrow:* *District Showdown Registration*! If you are participating in another alliance, please inform R4/R5 and you can move to the other alliance after Pompeii. Don't leave it to the last minute!")
                evening_msgs.append(f"📢 *Tomorrow:* *Archipelago Raid (AR)*!\n{REE_USERNAME} (R4), would you like to remind everyone in-game to register?")
            elif tomorrow_week_num == 4:
                evening_msgs.append(f"📢 *Tomorrow:* *Island Raid (IR)*!\n{REE_USERNAME} (R4), would you like to remind everyone in-game to register?")
                 
        elif tomorrow == 3: # Amanhã é Quinta
            if is_last_week_of_month:
                evening_msgs.append("📢 *Tomorrow:* *Back Alley Doctor's Request* bosses! There is still time to finish your individual missions so we can summon the best bosses!")
                
        elif tomorrow == 5: # Amanhã é Sábado (Hoje é Sexta)
            if current_week_num == 4:
                evening_msgs.append(f"⏰ *Registration Reminder:* *Extreme Showdown*! \n{REE_USERNAME} (R4), would you like to remind everyone in-game to register if they haven't yet? The battle starts tomorrow (Saturday) at 13:00 UTC!")

        # --- PARTE 2: Fechamento do Dia (Hoje) ---
        if day_of_week == 6: # Domingo
            evening_msgs.append("🪙 *Arena of Doom*: Don't forget to use your coins! They expire at reset.")
            if current_week_num == 2: # Se for semana de District Showdown
                evening_msgs.append("🔑 *District Showdown*: Time to use your keys on the enemy alliance vault. Check with R4/R5 which alliance to attack.")
        
        if all_star_active:
            evening_msgs.append("⭐ *All-Star Night*: Check the rank and decide if you'll invest resources to climb higher before reset! Good luck!")
            
        if has_wasteland_today:
            evening_msgs.append("🏜️ *Wasteland*: Check the rank and decide whether to use Energy Cans or save them for the next event. Good luck!")
            
        # Biohazard (Sábado, quando não tem All-Star)
        if day_of_week == 5 and not all_star_active:
            evening_msgs.append("☣️ *Biohazard Frenzy*: Don't forget to use the Bio-Stabilizers in Quick Accumulation to climb higher in the rank. Good luck!")
            
        # Se não houver nenhum aviso (Rede de Segurança)
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
