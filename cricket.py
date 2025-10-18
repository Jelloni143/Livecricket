import os
import time
import threading
import requests
import telebot

# ===== CONFIG =====
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("CRICKET_API_KEY")
API_URL = f"https://api.cricketdata.org/currentMatches?apikey={API_KEY}"

bot = telebot.TeleBot(BOT_TOKEN)

# ===== FUNCTIONS =====
def fetch_live_matches():
    try:
        resp = requests.get(API_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        matches = data.get("data") or data.get("matches") or []
        return matches
    except Exception as e:
        print("Error fetching matches:", e)
        return []

def format_matches_reply(matches):
    if not matches:
        return "⚠️ Koi live match nahi chal raha abhi."
    reply = "🔥 LIVE MATCHES 🔥\n\n"
    for m in matches[:5]:  # first 5 matches
        team1 = m.get('team1', {}).get('name', "Team1")
        team2 = m.get('team2', {}).get('name', "Team2")
        score1 = m.get('team1', {}).get('score', "N/A")
        score2 = m.get('team2', {}).get('score', "N/A")
        status = m.get('status', "Status N/A")
        reply += f"{team1} 🆚 {team2}\nScore: {score1} ‑ {score2}\nStatus: {status}\n\n"
    return reply

# ===== COMMAND HANDLERS =====
@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.reply_to(message, "🏏 Cricket Bot Ready!\nType /live to see live matches.")

@bot.message_handler(commands=['live'])
def cmd_live(message):
    matches = fetch_live_matches()
    reply = format_matches_reply(matches)
    bot.reply_to(message, reply)

# ===== AUTO-REFRESH THREAD =====
def auto_refresh(chat_id, interval=300):
    """Send match updates every 'interval' seconds."""
    while True:
        matches = fetch_live_matches()
        reply = format_matches_reply(matches)
        bot.send_message(chat_id, reply, parse_mode="HTML")
        time.sleep(interval)

@bot.message_handler(commands=['notify'])
def cmd_notify(message):
    chat_id = message.chat.id
    bot.reply_to(message, "🔔 Notifications enabled: Har 5 minute me update milegi.")
    threading.Thread(target=auto_refresh, args=(chat_id,), daemon=True).start()

# ===== RUN BOT =====
print("✅ Telegram Cricket Bot Running…")
bot.infinity_polling()
