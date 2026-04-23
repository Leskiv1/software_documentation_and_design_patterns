import csv

class DataReader:
    @staticmethod
    def read_csv(file_path: str):
        data = []
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
            print(f"[Reader] Успішно прочитано {len(data)} рядків з {file_path}")
            return data
        except FileNotFoundError:
            print(f"[Reader] Помилка: Файл {file_path} не знайдено!")
            return []
        except Exception as e:
            print(f"[Reader] Сталася помилка: {e}")
            return []