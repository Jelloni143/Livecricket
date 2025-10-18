from flask import Flask, request
import requests
import os

# ===== CONFIG =====
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Telegram bot token
API_KEY = os.environ.get("CRICKET_API_KEY")  # CricketData.org API key
CRICKET_API_URL = f"https://api.cricketdata.org/currentMatches?apikey={API_KEY}"

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__)

# ===== FUNCTIONS =====
def send_message(chat_id, text):
    """Send message to Telegram chat."""
    try:
        requests.post(f"{API_URL}/sendMessage", data={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        })
    except Exception as e:
        print("Telegram send error:", e)

def fetch_live_matches():
    """Fetch live matches from CricketData.org"""
    try:
        resp = requests.get(CRICKET_API_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data") or data.get("matches") or []
    except Exception as e:
        print("Error fetching matches:", e)
        return []

def format_matches(matches):
    """Format live matches to readable text."""
    if not matches:
        return "⚠️ Abhi koi live match nahi chal raha."
    reply = "🔥 LIVE MATCHES 🔥\n\n"
    for m in matches[:5]:  # top 5 matches
        team1 = m.get('team1', {}).get('name', "Team1")
        team2 = m.get('team2', {}).get('name', "Team2")
        score1 = m.get('team1', {}).get('score', "N/A")
        score2 = m.get('team2', {}).get('score', "N/A")
        status = m.get('status', "Status N/A")
        reply += f"{team1} 🆚 {team2}\nScore: {score1} - {score2}\nStatus: {status}\n\n"
    return reply

# ===== WEBHOOK =====
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    if "message" not in data:
        return {"ok": True}

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")

    if text.startswith("/start"):
        send_message(chat_id, "🏏 Cricket Bot Ready!\nType /live to see live matches.")
    elif text.startswith("/live"):
        matches = fetch_live_matches()
        send_message(chat_id, format_matches(matches))
    else:
        send_message(chat_id, "Unknown command. Try /live.")

    return {"ok": True}

@app.route("/")
def home():
    return "🏏 Cricket Bot is Running! 🚀"

# ===== RUN =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)    return reply

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
