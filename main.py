import asyncio
from ml.predictor import MLService
from trading.engine import TradeEngine
from data.replicator import DataReplicator
from data.snowflake import SnowflakeAnalytics
from utils.config import config
from utils.logger import logger

class SteamTrader:
    def __init__(self):
        self.ml = MLService()
        self.engine = TradeEngine()
        self.replicator = DataReplicator()
        self.analytics = SnowflakeAnalytics()
    
    async def run(self):
        logger.info("Starting SteamTrader PRO")
        while True:
            market_data = await self._fetch_market_data()
            prediction = await self.ml.predict(market_data)
            trade_result = await self.engine.execute_trade({
                **market_data,
                'predicted': prediction
            })
            if trade_result:
                await self.replicator.replicate(trade_result)
                await self.analytics.log_trade(trade_result)

async def main():
    trader = SteamTrader()
    await trader.engine.load_strategy('strategies/pro_strategy.wasm')
    await trader.run()

if __name__ == "__main__":
    asyncio.run(main())