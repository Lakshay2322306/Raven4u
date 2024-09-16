import re
import requests
from flask import Flask, request, jsonify, render_template
from faker import Faker
import os
import random
from telegram import Update, Bot
from telegram.ext import CommandHandler, CallbackContext, Updater

app = Flask(__name__)

# Initialize Faker for generating fake data
faker = Faker()

# Owner details (can be fetched from environment variables)
OWNER_ID = os.getenv("OWNER_ID", "123456789")
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "owner_name")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Telegram bot setup
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def clean(message):
    return message.strip()

def luhn_check(bin_number):
    """Returns True if the BIN is valid according to the Luhn algorithm."""
    sum_digits = 0
    num_digits = len(bin_number)
    odd_even = num_digits & 1

    for i in range(num_digits):
        digit = int(bin_number[i])
        if (i & 1) ^ odd_even:
            digit = digit * 2
            if digit > 9:
                digit -= 9
        sum_digits += digit

    return (sum_digits % 10) == 0

def get_bin_details(bin_number):
    """Send POST request to external BIN service to get BIN details."""
    url = 'http://bins.su/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0'
    }
    data = {
        'action': 'searchbins',
        'bins': bin_number,
        'bank': '',
        'country': ''
    }

    response = requests.post(url, headers=headers, data=data)

    # Parse the result with regex
    try:
        bank = clean(re.search(r'<td>Bank</td></tr><tr><td>(.*?)</td>', response.text).group(1))
        country = clean(re.search(fr'<td>{bank}</td><td>(.*?)</td>', response.text).group(1))
        brand = clean(re.search(fr'<td>{country}</td><td>(.*?)</td>', response.text).group(1))
        level = clean(re.search(fr'<td>{brand}</td><td>(.*?)</td>', response.text).group(1))
        card_type = clean(re.search(fr'<td>{level}</td><td>(.*?)</td>', response.text).group(1))
        return {
            'bin': bin_number,
            'bank': bank,
            'country': country,
            'brand': brand,
            'level': level,
            'type': card_type
        }
    except AttributeError:
        return None

def generate_fake_ip():
    """Generates a random IP address."""
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

def ipgen(amount=10):
    """Generates a list of fake IP addresses."""
    return [generate_fake_ip() for _ in range(amount)]

# Telegram bot command handlers
def start(update: Update, context: CallbackContext):
    """Handle the /start command."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="👋 Welcome! Use /help to see available commands.")

def help_command(update: Update, context: CallbackContext):
    """Handle the /help command."""
    help_text = (
        "🛠️ **Available Commands:**\n"
        "/start - Start the bot\n"
        "/ping - Test the ping endpoint\n"
        "/check_id - Get owner ID and username\n"
        "/generate_fake_details - Generate fake personal details\n"
        "/generate_ip - Generate fake IP addresses\n"
        "/generate_username - Generate a fake username\n"
        "/generate_company - Generate a fake company name\n"
        "/bot_token - Get the bot token (owner only)\n"
        "/joke - Get a random joke\n"
        "/quote - Get a random inspirational quote"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

def ping(update: Update, context: CallbackContext):
    """Handle the /ping command."""
    response = requests.get("http://your-flask-app-url/ping")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"🔄 {response.text}")

def check_id(update: Update, context: CallbackContext):
    """Handle the /check_id command."""
    response = requests.get("http://your-flask-app-url/check_id")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"👤 {response.text}")

def generate_fake_details(update: Update, context: CallbackContext):
    """Handle the /generate_fake_details command."""
    response = requests.get("http://your-flask-app-url/faker")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"📋 {response.text}")

def generate_ip(update: Update, context: CallbackContext):
    """Handle the /generate_ip command."""
    amount = int(context.args[0]) if context.args else 10
    response = requests.get(f"http://your-flask-app-url/ipgen?amount={amount}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"🌐 {response.text}")

def generate_username(update: Update, context: CallbackContext):
    """Handle the /generate_username command."""
    response = requests.get("http://your-flask-app-url/generate_username")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"👤 {response.text}")

def generate_company(update: Update, context: CallbackContext):
    """Handle the /generate_company command."""
    response = requests.get("http://your-flask-app-url/generate_company")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"🏢 {response.text}")

def bot_token(update: Update, context: CallbackContext):
    """Handle the /bot_token command."""
    if context.args and context.args[0] == OWNER_ID:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"🔑 Bot Token: {BOT_TOKEN}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Unauthorized")

def joke(update: Update, context: CallbackContext):
    """Handle the /joke command."""
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    joke_data = response.json()
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"😂 {joke_data['setup']} - {joke_data['punchline']}")

def quote(update: Update, context: CallbackContext):
    """Handle the /quote command."""
    response = requests.get("https://api.quotable.io/random")
    quote_data = response.json()
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"💬 \"{quote_data['content']}\" — {quote_data['author']}")

# Add command handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help_command))
dispatcher.add_handler(CommandHandler('ping', ping))
dispatcher.add_handler(CommandHandler('check_id', check_id))
dispatcher.add_handler(CommandHandler('generate_fake_details', generate_fake_details))
dispatcher.add_handler(CommandHandler('generate_ip', generate_ip))
dispatcher.add_handler(CommandHandler('generate_username', generate_username))
dispatcher.add_handler(CommandHandler('generate_company', generate_company))
dispatcher.add_handler(CommandHandler('bot_token', bot_token))
dispatcher.add_handler(CommandHandler('joke', joke))
dispatcher.add_handler(CommandHandler('quote', quote))

# Start the Telegram bot
updater.start_polling()

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping', methods=['GET'])
def ping():
    return "Pong!", 200

@app.route('/check_id', methods=['GET'])
def check_id():
    return jsonify({
        "owner_id": OWNER_ID,
        "owner_username": OWNER_USERNAME
    }), 200

@app.route('/bin', methods=['POST'])
def bin_lookup():
    data = request.json
    if not data or 'bin' not in data:
        return jsonify({"error": "BIN not provided"}), 400

    bin_number = data['bin'][:6]  # First 6 digits are the BIN
    if not luhn_check(bin_number):
        return jsonify({"error": "Invalid BIN (failed Luhn check)"}), 400

    bin_details = get_bin_details(bin_number)
    if bin_details:
        return jsonify(bin_details), 200
    else:
        return jsonify({"error": "BIN details not found"}), 404

@app.route('/faker', methods=['GET'])
def generate_fake_details():
    fake_data = {
        "name": faker.name(),
        "address": faker.address(),
        "country": faker.country(),
        "zip_code": faker.zipcode(),
        "email": faker.email(),
        "phone_number": faker.phone_number(),
