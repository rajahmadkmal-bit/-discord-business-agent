import discord
import os
from google import genai
from dotenv import load_dotenv

# Load API keys from .env files
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Business FAQ knowledge base
FAQS = {
    "timing": "Our business hours are 9 AM to 6 PM, Monday through Saturday.",
    "hours": "Our business hours are 9 AM to 6 PM, Monday through Saturday.",
    "location": "We are based in Lahore, Pakistan.",
    "address": "We are based in Lahore, Pakistan.",
    "contact": "You can reach us at +92 XXX XXXXXXX or via email.",
    "pricing": "Please share more details about your requirements, and our team will provide a customized quote.",
}

# System prompt to keep the agent professional
SYSTEM_PROMPT = (
    "You are a professional customer support assistant for a business. "
    "Always respond in clear, polite, professional English. "
    "Keep responses concise and helpful. "
    "If you don't have specific information, politely ask the customer "
    "to provide more details or offer to connect them with the team."
)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)

@discord_client.event
async def on_ready():
    print(f"Bot is ready! Logged in as {discord_client.user}")

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    user_text = message.content.lower()

    # Check FAQs first (fast, no API call needed)
    for key, answer in FAQS.items():
        if key in user_text:
            await message.channel.send(answer)
            return

    # Otherwise, generate a professional response using Gemini
    try:
        prompt = f"{SYSTEM_PROMPT}\n\nCustomer message: {message.content}"
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        await message.channel.send(response.text)
    except Exception as e:
        await message.channel.send(
            "I apologize, but I'm experiencing a technical issue right now. "
            "Please try again shortly."
        )
        print(f"Error: {e}")

discord_client.run(DISCORD_TOKEN)