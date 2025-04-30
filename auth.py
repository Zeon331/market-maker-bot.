import aiohttp
import re
import configparser
from steam.client import SteamClient
from steam.enums import EResult

config = configparser.ConfigParser()
config.read('config.ini')

class SteamAuth:
    def __init__(self):
        self.client = SteamClient()
        self.session = None
        self.requires_2fa = False
        self.balance = 0.0
        self.csrf_token = ""
        self.login_attempts = 0

    async def create_session(self):
        """Создание aiohttp сессии"""
        self.session = aiohttp.ClientSession()

    async def login(self, username: str, password: str) -> bool:
        """Основной метод авторизации"""
        try:
            if self.login_attempts >= int(config['requests'].get('max_attempts', 3)):
                raise PermissionError("Too many login attempts")
            
            # Явная установка учетных данных
            self.client.username = username
            self.client.password = password
            
            result = self.client.login()
            
            if result == EResult.OK:
                await self._update_session()
                return True
                
            if result == EResult.AccountLoginDeniedNeedTwoFactor:
                self.requires_2fa = True
                return True
                
            raise ConnectionError(f"Login failed with code: {result.name}")
        except Exception as e:
            self.login_attempts += 1
            raise RuntimeError(f"Login error: {str(e)}") from e

    async def submit_2fa(self, code: str) -> bool:
        """Отправка кода Steam Guard"""
        try:
            result = self.client.login(two_factor_code=code)
            if result == EResult.OK:
                await self._update_session()
                return True
            return False
        except Exception as e:
            raise RuntimeError(f"2FA error: {str(e)}") from e

    async def _update_session(self):
        """Обновление данных сессии"""
        if not self.session:
            await self.create_session()
        
        # Обновление куков
        self.session.cookie_jar.update_cookies(self.client.get_cookies())
        
        # Получение баланса и CSRF
        async with self.session.get("https://steamcommunity.com/market") as resp:
            text = await resp.text()
            self._parse_session_data(text)

    def _parse_session_data(self, text: str):
        """Парсинг ключевых данных из HTML"""
        try:
            # Поиск баланса
            balance_match = re.search(r'g_strWalletBalance\s*=\s*"([\d\.]+)"', text)
            if balance_match:
                self.balance = float(balance_match.group(1))
            
            # Поиск CSRF-токена
            csrf_match = re.search(r'g_sessionID\s*=\s*"([\w-]+)"', text)
            if csrf_match:
                self.csrf_token = csrf_match.group(1)
        except Exception as e:
            raise ValueError(f"Session data parsing error: {str(e)}") from e

    async def update_balance(self) -> float:
        """Обновление баланса через API"""
        try:
            async with self.session.get("https://steamcommunity.com/market") as resp:
                text = await resp.text()
                self._parse_session_data(text)
                return self.balance
        except Exception as e:
            raise ConnectionError(f"Balance update failed: {str(e)}") from e

    async def close(self):
        """Корректное закрытие сессии"""
        if self.session:
            await self.session.close()