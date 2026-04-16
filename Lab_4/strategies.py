import json
import redis
from kafka import KafkaProducer
from abc import ABC, abstractmethod
import firebase_admin
from firebase_admin import credentials, firestore

# ==========================================
# 1. Інтерфейс Стратегії (Базовий клас)
# ==========================================
class AbstractOutputStrategy(ABC):
    @abstractmethod
    def write(self, data: list):
        """Кожна стратегія повинна мати цей метод"""
        pass

    def _extract_info(self, row: dict):
        """Допоміжний метод для витягування ID та Типу з рядка CSV"""
        uid = row.get("unique_id", row.get("collision_id", "N/A"))
        v_type = row.get("vehicle_type_code1", row.get("vehicle_type_code_1", row.get("vehicle_type", "Unknown")))

        if not v_type:
            v_type = "Unknown"

        return uid, v_type


# ==========================================
# 2. Конкретна Стратегія А: Вивід у Консоль
# ==========================================
class ConsoleStrategy(AbstractOutputStrategy):
    def write(self, data: list):
        print(f"\n--- [ConsoleStrategy] Виводимо перші 10 записів ---")

        for row in data[:10]:
            uid, v_type = self._extract_info(row)
            print(f"[CONSOLE] ID: {uid} | Type: {v_type}")

        print(f"--- Всього оброблено рядків: {len(data)} ---\n")


# ==========================================
# 3. Конкретна Стратегія Б: Запис у Redis
# ==========================================
class RedisStrategy(AbstractOutputStrategy):
    def __init__(self, host: str, port: int):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def write(self, data: list):
        print(f"\n[RedisStrategy] Підключення до Redis ({self.client.ping()})...")
        list_name = "nyc_collisions_list"

        self.client.delete(list_name)

        for i, row in enumerate(data):
            self.client.rpush(list_name, json.dumps(row))

            if i < 10:
                uid, v_type = self._extract_info(row)
                print(f"[REDIS] Збережено -> ID: {uid} | Type: {v_type}")

        if len(data) > 10:
            print(f"... і ще {len(data) - 10} записів збережено.")

        print(f"[RedisStrategy] Успішно записано {len(data)} рядків у ключ '{list_name}'\n")


# ==========================================
# 4. Конкретна Стратегія В: Відправка в Kafka
# ==========================================
class KafkaStrategy(AbstractOutputStrategy):
    def __init__(self, bootstrap_servers: str, topic: str):
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version=(2, 8, 1)
        )

    def write(self, data: list):
        print(f"\n[KafkaStrategy] Відправка повідомлень у топік '{self.topic}'...")

        for i, row in enumerate(data):
            self.producer.send(self.topic, value=row)

            if i < 10:
                uid, v_type = self._extract_info(row)
                print(f"[KAFKA] Відправлено -> ID: {uid} | Type: {v_type}")

        self.producer.flush()

        if len(data) > 10:
            print(f"... і ще {len(data) - 10} повідомлень відправлено.")

        print(f"[KafkaStrategy] Успішно відправлено {len(data)} повідомлень\n")


# ==========================================
# 5. Конкретна Стратегія Г: Запис у Firestore
# ==========================================
class FirestoreStrategy(AbstractOutputStrategy):
    def __init__(self, key_path: str, project_id: str, collection_name: str):
        self.collection_name = collection_name

        if not firebase_admin._apps:
            print(f"[FirestoreStrategy] Ініціалізація підключення (Project ID: {project_id})...")
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred, {'projectId': project_id})

        self.db = firestore.client()

    def write(self, data: list):
        print(f"\n[FirestoreStrategy] Відправка даних у колекцію '{self.collection_name}'...")

        collection_ref = self.db.collection(self.collection_name)

        for i, row in enumerate(data):
            uid, v_type = self._extract_info(row)

            if uid != "N/A":
                collection_ref.document(str(uid)).set(row)
            else:
                collection_ref.add(row)

            if i < 10:
                print(f"[FIRESTORE] Збережено -> ID: {uid} | Type: {v_type}")

        if len(data) > 10:
            print(f"... і ще {len(data) - 10} документів збережено у хмару")

        print(f"[FirestoreStrategy] Успішно записано {len(data)} документів у Firestore\n")