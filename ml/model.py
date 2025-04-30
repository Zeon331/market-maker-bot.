import torch
import torch.nn as nn
from utils.logger import logger

class PricePredictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(10, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
        logger.info("ML model initialized")

    def forward(self, x):
        return self.layers(x)