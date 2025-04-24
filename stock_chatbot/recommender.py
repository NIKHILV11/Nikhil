import requests
from bs4 import BeautifulSoup

def get_stockrecommendations():
    url = "https://www.moneycontrol.com/stocks/marketstats/nsegainer/index.php"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table", class_="tbldata14")

        if not table:
            raise ValueError("Could not find gainer table on page.")

        rows = table.find_all("tr")[1:6]  # Top 5 gainers
        recommendations = []

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 5:
                symbol = cols[0].text.strip()
                last_price = cols[1].text.strip()
                change_pct = cols[4].text.strip()

                recommendations.append({
                    "symbol": symbol,
                    "action": "BUY",
                    "reason": f"Gaining {change_pct} today. Price: ₹{last_price}"
                })

        return recommendations

    except Exception as e:
        print(f"Error scraping stock recommendations: {e}")
        return [{"symbol": "N/A", "action": "HOLD", "reason": "Recommendation data not available currently."}]

def get_sellrecommendations():
    url = "https://www.moneycontrol.com/stocks/marketstats/nseloser/index.php"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table", class_="tbldata14")

        if not table:
            raise ValueError("Could not find loser table on page.")

        rows = table.find_all("tr")[1:6]  # Top 5 losers
        recommendations = []

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 5:
                symbol = cols[0].text.strip()
                last_price = cols[1].text.strip()
                change_pct = cols[4].text.strip()

                recommendations.append({
                    "symbol": symbol,
                    "action": "SELL",
                    "reason": f"Dropped {change_pct} today. Price: ₹{last_price}"
                })

        return recommendations

    except Exception as e:
        print(f"Error scraping stock sell suggestions: {e}")
        return [{"symbol": "N/A", "action": "HOLD", "reason": "Sell data not available."}]