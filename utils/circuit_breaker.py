from pybreaker import CircuitBreaker
from utils.logger import logger

class TradingBreaker(CircuitBreaker):
    def __init__(self):
        super().__init__(
            fail_max=5,
            reset_timeout=60,
            listeners=[TradingBreakerListener()]
        )

class TradingBreakerListener:
    def state_change(self, cb, old_state, new_state):
        logger.warning(
            "Circuit Breaker state changed",
            old_state=old_state.name,
            new_state=new_state.name
        )