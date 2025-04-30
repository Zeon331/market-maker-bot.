import os
import hvac
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.vault_client = hvac.Client(
            url=os.getenv('VAULT_ADDR'),
            token=os.getenv('VAULT_TOKEN')
        )
        
        self._secrets = self.vault_client.secrets.kv.v2.read_secret_version(
            path='steam-trader/prod'
        )['data']['data']
    
    @property
    def snowflake_config(self):
        return {
            'user': self._secrets['SNOWFLAKE_USER'],
            'password': self._secrets['SNOWFLAKE_PASS'],
            'account': self._secrets['SNOWFLAKE_ACCOUNT']
        }
    
    @property
    def model_params(self):
        return {
            'batch_size': 64,
            'gpu_enabled': True
        }

config = Config()