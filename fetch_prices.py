#!/usr/bin/env python3
"""
Fetch all crypto prices from CoinGecko and save to prices.txt
Runs every 5 minutes via GitHub Actions
"""

import requests
import json
import os
from datetime import datetime

# CoinGecko API - free tier, no API key needed for basic usage
COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"

# Parameters: get top 250 coins by market cap
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 250,
    "page": 1,
    "sparkline": "false",
    "price_change_percentage": "24h,7d,30d"
}

OUTPUT_FILE = "prices.txt"

def fetch_prices():
    """Fetch crypto prices from CoinGecko"""
    try:
        response = requests.get(COINGECKO_URL, params=PARAMS, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching prices: {e}")
        return None

def format_price(data):
    """Format price data for txt file"""
    lines = []
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    lines.append(f"# Crypto Prices - Updated: {timestamp}")
    lines.append(f"# Source: CoinGecko API")
    lines.append(f"# Total coins: {len(data)}")
    lines.append("")
    
    for coin in data:
        symbol = coin.get('symbol', '').upper()
        name = coin.get('name', '')
        current_price = coin.get('current_price', 0) or 0
        market_cap = coin.get('market_cap', 0) or 0
        volume_24h = coin.get('total_volume', 0) or 0
        change_24h = coin.get('price_change_percentage_24h', 0) or 0
        change_7d = coin.get('price_change_percentage_7d_in_currency', 0) or 0
        change_30d = coin.get('price_change_percentage_30d_in_currency', 0) or 0
        
        # Format: SYMBOL|NAME|PRICE|MARKET_CAP|VOLUME_24H|CHANGE_24H|CHANGE_7D|CHANGE_30D
        line = f"{symbol}|{name}|{current_price:.8f}|{market_cap:.0f}|{volume_24h:.0f}|{change_24h:.2f}|{change_7d:.2f}|{change_30d:.2f}"
        lines.append(line)
    
    return "\n".join(lines)

def main():
    print("Fetching crypto prices...")
    data = fetch_prices()
    
    if data is None:
        print("Failed to fetch prices!")
        return 1
    
    content = format_price(data)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Saved {len(data)} coins to {OUTPUT_FILE}")
    print(f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    return 0

if __name__ == "__main__":
    exit(main())