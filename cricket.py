from flask import Flask, request
import requests
import os
import random

app = Flask(__name__)

# ===== CONFIG =====
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CRICKET_API_KEY = os.environ.get("CRICKET_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")  # NewsAPI.org key
CRICKET_API_URL = f"https://api.cricketdata.org/currentMatches?apikey={CRICKET_API_KEY}"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ===== FUNCTIONS =====
def send_message(chat_id, text):
    try:
        requests.post(f"{API_URL}/sendMessage", data={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        })
    except Exception as e:
        print("Error sending Telegram message:", e)

# ----- API FEATURES -----
def fetch_live_matches():
    try:
        resp = requests.get(CRICKET_API_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data") or data.get("matches") or []
    except Exception as e:
        print("Cricket API error:", e)
        return []

def format_matches(matches):
    if not matches:
        return "⚠️ Abhi koi live match nahi chal raha."
    reply = "🔥 LIVE MATCHES 🔥\n\n"
    for m in matches[:5]:
        team1 = m.get('team1', {}).get('name', "Team1")
        team2 = m.get('team2', {}).get('name', "Team2")
        score1 = m.get('team1', {}).get('score', "N/A")
        score2 = m.get('team2', {}).get('score', "N/A")
        status = m.get('status', "Status N/A")
        reply += f"{team1} 🆚 {team2}\nScore: {score1} - {score2}\nStatus: {status}\n\n"
    return reply

def get_joke():
    try:
        r = requests.get("https://official-joke-api.appspot.com/jokes/random", timeout=5)
        data = r.json()
        return f"{data.get('setup')} 🤣 {data.get('punchline')}"
    except:
        return "😅 Joke API error, try again later!"

def get_quote():
    try:
        r = requests.get("https://zenquotes.io/api/random", timeout=5)
        data = r.json()[0]
        return f"{data.get('q')} — {data.get('a')}"
    except:
        return "Quote API error, try again later!"

def get_advice():
    try:
        r = requests.get("https://api.adviceslip.com/advice", timeout=5)
        data = r.json()
        return data.get("slip", {}).get("advice", "Advice not available")
    except:
        return "Advice API error!"

def get_fact():
    try:
        r = requests.get("https://uselessfacts.jsph.pl/random.json?language=en", timeout=5)
        data = r.json()
        return data.get("text", "Fact not available")
    except:
        return "Fact API error!"

def get_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&pageSize=3"
        r = requests.get(url, timeout=5)
        data = r.json()
        articles = data.get("articles", [])
        reply = "📰 Top News:\n\n"
        for a in articles:
            reply += f"{a.get('title')}\n{a.get('url')}\n\n"
        return reply if articles else "No news available"
    except:
        return "News API error!"

def get_meditation():
    tips = [
        "अपनी आंखें बंद करो और 5 मिनट सांसों पर ध्यान दो 🧘‍♂️",
        "संतुलित शरीर और मन के लिए रोज़ 10 मिनट मेडिटेशन करो 🌿"
    ]
    return random.choice(tips)

def translate_text(text):
    # Dummy translation for free version
    return f"Translated (English->Hindi): {text} [हिंदी में]"

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
        send_message(chat_id, "👋 Axel Bot Ready!\nCommands:\n/live /joke /quote /tip /meditation /fact /advice /riddle /news /translate")
    elif text.startswith("/live"):
        matches = fetch_live_matches()
        send_message(chat_id, format_matches(matches))
    elif text.startswith("/joke"):
        send_message(chat_id, get_joke())
    elif text.startswith("/quote"):
        send_message(chat_id, get_quote())
    elif text.startswith("/tip"):
        send_message(chat_id, get_advice())
    elif text.startswith("/meditation"):
        send_message(chat_id, get_meditation())
    elif text.startswith("/fact"):
        send_message(chat_id, get_fact())
    elif text.startswith("/advice"):
        send_message(chat_id, get_advice())
    elif text.startswith("/news"):
        send_message(chat_id, get_news())
    elif text.startswith("/translate"):
        msg_to_translate = text.replace("/translate","").strip()
        if msg_to_translate:
            send_message(chat_id, translate_text(msg_to_translate))
        else:
            send_message(chat_id, "Use: /translate <text>")
    else:
        send_message(chat_id, "Unknown command. Try /live or /joke")

    return {"ok": True}

@app.route("/")
def home():
    return "🛡️ Multi-Feature API Bot is Running! 🚀"

# ===== RUN =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)def format_matches(matches):
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
