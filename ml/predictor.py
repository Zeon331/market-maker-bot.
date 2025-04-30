import torch
import numpy as np
from .model import PricePredictor
from utils.logger import logger

class MLService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = PricePredictor().to(self.device)
        logger.info(f"ML Service initialized on {self.device}")
    
    async def predict(self, data):
        try:
            tensor_data = self._preprocess(data)
            with torch.no_grad():
                prediction = self.model(tensor_data)
            return prediction.cpu().numpy()
        except Exception as e:
            logger.error("Prediction failed", exc_info=True)
            raise
    
    def _preprocess(self, data):
        return torch.tensor(data, device=self.device, dtype=torch.float32)