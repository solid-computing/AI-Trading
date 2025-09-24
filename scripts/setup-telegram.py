#!/usr/bin/env python3
"""
Utility script to help setup Telegram bot integration.
This script helps you get your chat ID and test the bot connection.
"""

import json
import requests
import sys

def get_chat_id(bot_token):
    """Get chat ID by sending a message to the bot"""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if not data.get('ok'):
            print(f"Error: {data.get('description', 'Unknown error')}")
            return None
            
        updates = data.get('result', [])
        if not updates:
            print("No messages found. Send a message to your bot first.")
            return None
            
        # Get the most recent chat ID
        chat_id = updates[-1]['message']['chat']['id']
        return chat_id
        
    except requests.RequestException as e:
        print(f"Error connecting to Telegram API: {e}")
        return None

def test_bot(bot_token, chat_id):
    """Test sending a message to the bot"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    data = {
        'chat_id': chat_id,
        'text': '🤖 Freqtrade bot test message! Your bot is configured correctly.'
    }
    
    try:
        response = requests.post(url, data=data)
        result = response.json()
        
        if result.get('ok'):
            print("✅ Test message sent successfully!")
            return True
        else:
            print(f"❌ Error sending message: {result.get('description')}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Error connecting to Telegram API: {e}")
        return False

def main():
    """Main function"""
    print("🤖 Freqtrade Telegram Bot Setup Helper")
    print("=" * 40)
    
    if len(sys.argv) != 2:
        print("Usage: python setup-telegram.py <BOT_TOKEN>")
        print("\nTo get a bot token:")
        print("1. Message @BotFather on Telegram")
        print("2. Use /newbot command")
        print("3. Follow the instructions")
        print("4. Copy the token and run this script")
        sys.exit(1)
    
    bot_token = sys.argv[1]
    
    print("Step 1: Getting your Chat ID...")
    print("Please send a message to your bot now, then press Enter")
    input()
    
    chat_id = get_chat_id(bot_token)
    if not chat_id:
        print("❌ Could not get Chat ID. Make sure you sent a message to your bot.")
        sys.exit(1)
    
    print(f"✅ Found Chat ID: {chat_id}")
    
    print("\nStep 2: Testing bot connection...")
    if test_bot(bot_token, chat_id):
        print("\n🎉 Setup successful!")
        print("\nAdd these to your environment variables:")
        print(f"TELEGRAM_TOKEN={bot_token}")
        print(f"TELEGRAM_CHAT_ID={chat_id}")
        
        print("\nFor CircleCI, add these to your 'freqtrade-secrets' context:")
        print(f"- TELEGRAM_TOKEN: {bot_token}")
        print(f"- TELEGRAM_CHAT_ID: {chat_id}")
    else:
        print("\n❌ Setup failed. Please check your bot token and try again.")

if __name__ == "__main__":
    main()