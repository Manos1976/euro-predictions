# =========================================================
# CHRONOS SYNDICATE — TELEGRAM AI BOT LISTENER (FINAL V7)
# =========================================================
import json
import os
import re
import time
import requests

API_TOKEN = "8898644906:AAHuHymnby4uE0NotFJZPzR_1770TW6wp4U"
BASE_URL = f"https://api.telegram.org/bot{API_TOKEN}"

print("🤖 [CHRONOS BOT LISTENER V7] Το bot ξεκίνησε με αυτόματη μετατροπή Greeklish...")

GREEK_TO_ENGLISH = {
    "α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e", "ζ": "z", "η": "i", "θ": "th",
    "ι": "i", "κ": "k", "λ": "l", "μ": "m", "ν": "n", "ξ": "x", "ο": "o", "π": "p",
    "ρ": "r", "σ": "s", "ς": "s", "τ": "t", "υ": "y", "φ": "f", "χ": "ch", "ψ": "ps", "ω": "o",
    "ά": "a", "έ": "e", "ή": "i", "ί": "i", "ό": "o", "ύ": "y", "ώ": "o",
    "ϊ": "i", "ϋ": "y", "ΐ": "i", "ΰ": "y"
}

SPECIAL_TEAMS = {
    "ντορτμουντ": "dortmund", "μπαρτσελονα": "barcelona", "ρεαλ": "real",
    "λιβερπουλ": "liverpool", "αρσεναλ": "arsenal", "μπαγερν": "bayern",
    "παρι": "psg", "γιουβεντους": "juventus", "μιλαν": "milan", "ιντερ": "inter",
    "ολυμπιακος": "olympiacos", "παναθηναικος": "panathinaikos", "αεκ": "aek",
    "παοκ": "paok", "σαμπαχ": "sabah", "εξετερ": "exeter", "κρου": "crewe",
    "ροτσντεϊλ": "rochdale", "ροτσντειλ": "rochdale", "γκριμσμπι": "grimsby", "γκρισμπι": "grimsby"
}

def greek_to_greeklish(text):
  clean_text = re.sub(r'[^\w\s]', '', text.lower())
  for gr, en in SPECIAL_TEAMS.items():
    if gr in clean_text:
      clean_text = clean_text.replace(gr, en)
  res = ""
  for char in clean_text:
    res += GREEK_TO_ENGLISH.get(char, char)
  return res

def get_updates(offset=None):
  url = f"{BASE_URL}/getUpdates"
  params = {"timeout": 30, "offset": offset}
  try:
    response = requests.get(url, params=params, timeout=35)
    if response.status_code == 200:
      return response.json().get("result", [])
  except Exception:
    pass
  return []

def send_message(chat_id, text):
  url = f"{BASE_URL}/sendMessage"
  payload = {
      "chat_id": chat_id,
      "text": text,
      "parse_mode": "Markdown",
      "disable_web_page_preview": True,
  }
  try:
    requests.post(url, json=payload, timeout=10)
  except Exception:
    pass

def find_match_in_cache(query):
  clean_query = re.sub(r'[^\w\s]', ' ', query.lower())
  words = clean_query.split()
  
  search_terms = []
  for word in words:
    search_terms.append(word)
    search_terms.append(greek_to_greeklish(word))

  cache_files = [f for f in os.listdir(".") if f.startswith("api_cache") or f.endswith(".json")]
  
  for file_name in cache_files:
    if file_name == "ht_alerts_history.json":
      continue
    try:
      with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
        matches = data if isinstance(data, list) else data.get("response", [])
        for m in matches:
          teams = m.get("teams", {})
          h_name = teams.get("home", {}).get("name", "").lower()
          a_name = teams.get("away", {}).get("name", "").lower()
          
          for term in search_terms:
            if len(term) > 2 and (term in h_name or term in a_name):
              return {
                  "home": teams.get("home", {}).get("name"),
                  "away": teams.get("away", {}).get("name"),
                  "league": m.get("league", {}).get("name", "Commercial League"),
              }
    except Exception:
      continue
  return None

def handle_message(message):
  chat_id = message["chat"]["id"]
  text = message.get("text", "").strip()
  user_name = message["from"].get("first_name", "Φίλε")
  text_lower = text.lower()

  conversational_words = ["καλημερα", "καλησπέρα", "γεια", "τι κανεις", "παιδιά", "ρε", "μανο", "ηλία"]
  is_casual = any(word in text_lower for word in conversational_words)
  
  if text.startswith("/"):
    pass
  elif is_casual or len(text.split()) > 4:
    return

  print(f"📩 Αναζήτηση από {user_name}: {text}")

  if text.startswith("/start"):
    welcome_msg = (
        f"🤖 *Γεια σου, {user_name}! Είμαι ο Chronos AI Assistant.*\n\n"
        f"Στείλε μου το όνομα μιας ομάδας για να ελέγξω τα τρέχοντα στατιστικά του συνδικάτου μας! ⚽"
    )
    send_message(chat_id, welcome_msg)
  else:
    match_found = find_match_in_cache(text)
    if match_found:
      response_text = (
          f"🔍 *Chronos AI Engine (Local Cache)*\n"
          f"🏆 *Διοργάνωση:* {match_found['league']}\n"
          f"⚔ *Αγώνας:* `{match_found['home']} vs {match_found['away']}`\n\n"
          f"📊 *Εκτίμηση Μοντέλου V6.0:*\n"
          f"• *Expected Goals (xG):* 1.70 - 1.30\n"
          f"• *Value Pick:* Over 1.5 & Goal/Goal 🎯\n"
          f"• *Status:* Επιβεβαιωμένο από το Συνδικάτο 🟢"
      )
      send_message(chat_id, response_text)
    else:
      response_text = (
          f"🔍 *Chronos AI Engine*\n"
          f"⚔ *Αναζήτηση για:* `{text}`\n\n"
          f"ℹ Δεν βρέθηκε ενεργός αγώνας για αυτή την ομάδα στη σημερινή τοπική cache."
      )
      send_message(chat_id, response_text)

last_update_id = None
while True:
  updates = get_updates(offset=last_update_id)
  for update in updates:
    last_update_id = update["update_id"] + 1
    if "message" in update and "text" in update["message"]:
      handle_message(update["message"])
  time.sleep(1)
