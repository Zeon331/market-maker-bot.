import aiohttp  # Добавлен импорт
from urllib.parse import quote
from utils.rate_limiter import RateLimiter
from utils.proxy_manager import ProxyManager
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class SteamMarketAPI:
    def __init__(self, auth):
        self.auth = auth
        self.proxy = ProxyManager()
        self.limiters = {
            'price': RateLimiter(1, 1.0),
            'inventory': RateLimiter(1, 300),
            'general': RateLimiter(50, 60)
        }

    # ... остальной код ...

    async def get_listings(self):
        await self.limiters['general'].wait()
        url = f"https://steamcommunity.com/market/search/render/?appid={config['steam']['app_id']}&count=100"
        
        async with self.auth.session.get(url, proxy=self.proxy.next()) as resp:
            data = await resp.json()
            return data.get('results', [])

    async def get_price_history(self, item_name):
        await self.limiters['price'].wait()
        url = f"https://steamcommunity.com/market/pricehistory/?appid={config['steam']['app_id']}&market_hash_name={quote(item_name)}"
        
        async with self.auth.session.get(url, proxy=self.proxy.next()) as resp:
            return await resp.json()

    def is_profitable(self, item):
        history = self.get_price_history(item['name'])
        week_prices = [p[1] for p in history.get('prices', [])[-7:]]
        if not week_prices: return False
        
        median = sum(week_prices) / len(week_prices)
        profit = (item['sell_price'] * 0.85) / median
        return profit >= float(config['steam']['min_roi'])

    async def buy_item(self, item):
        await self.limiters['general'].wait()
        data = {
            'sessionid': self.auth.csrf_token,
            'currency': config['steam']['currency'],
            'quantity': 1
        }
        
        async with self.auth.session.post(
            f"https://steamcommunity.com/market/buylisting/{item['id']}",
            data=data,
            proxy=self.proxy.next()
        ) as resp:
            return (await resp.json()).get('success', False)
