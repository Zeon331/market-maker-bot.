import csv
from datetime import datetime

class CSVExporter:
    def __init__(self, filename="transactions.csv"):
        self.filename = filename
        self._init_file()
    
    def _init_file(self):
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Timestamp', 
                'Item Name', 
                'Purchase Price', 
                'Median Price', 
                'Commission', 
                'Profit'
            ])
    
    def log_transaction(self, item_data):
        row = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            item_data.get('name', 'N/A'),
            item_data.get('price', 0),
            item_data.get('median_price', 0),
            item_data.get('commission', 0),
            item_data.get('profit', 0)
        ]
        
        with open(self.filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)