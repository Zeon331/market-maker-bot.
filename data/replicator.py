import boto3
from utils.logger import logger

class DataReplicator:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.primary_bucket = 'steam-trader-data-eu'
        self.replica_buckets = ['steam-trader-data-us', 'steam-trader-data-asia']
    
    async def replicate(self, data):
        try:
            # Основное сохранение
            self.s3.put_object(
                Bucket=self.primary_bucket,
                Key=data['key'],
                Body=data['content']
            )
            
            # Асинхронная репликация
            for bucket in self.replica_buckets:
                self.s3.copy_object(
                    CopySource={'Bucket': self.primary_bucket, 'Key': data['key']},
                    Bucket=bucket,
                    Key=data['key']
                )
            logger.info("Data replicated globally")
        except Exception as e:
            logger.error("Replication failed", error=str(e))
            raise