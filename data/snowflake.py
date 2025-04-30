import snowflake.connector
from utils.config import config
from utils.logger import logger

class SnowflakeAnalytics:
    def __init__(self):
        self.conn = snowflake.connector.connect(
            user=config.snowflake_config['user'],
            password=config.snowflake_config['password'],
            account=config.snowflake_config['account']
        )
    
    async def log_trade(self, trade_data):
        try:
            query = """
                INSERT INTO trades VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                )
            """
            self.conn.cursor().execute(query, (
                trade_data['timestamp'],
                trade_data['item_id'],
                trade_data['price'],
                trade_data['predicted'],
                trade_data['strategy'],
                trade_data['profit'],
                trade_data['region']
            ))
            logger.info("Trade logged to Snowflake")
        except Exception as e:
            logger.error("Snowflake error", error=str(e))
            raise