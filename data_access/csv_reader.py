import csv
from typing import List, Dict, Any
from data_access.interfaces import IDataLoader

class CSVDataLoader(IDataLoader):
    def read_data(self, file_path: str) -> List[Dict[str, Any]]:
        """Зчитує дані з CSV файлу і повертає список словників."""
        data = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file) # DictReader автоматично бере заголовки стовпців як ключі
            for row in reader:
                data.append(row)
        return data