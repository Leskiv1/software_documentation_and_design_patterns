import json
import sys
import os
from dotenv import load_dotenv

from reader import DataReader
from strategies import ConsoleStrategy, RedisStrategy, KafkaStrategy, FirestoreStrategy

load_dotenv()


def load_config(config_path="config.json"):
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Помилка: Файл config.json не знайдено!")
        sys.exit(1)


def resolve_env_variable(value: str):
    """
    Якщо значення в конфігу починається з '$ENV_',
    ця функція дістане реальне значення з .env файлу.
    """
    if isinstance(value, str) and value.startswith("$ENV_"):
        env_key = value.replace("$ENV_", "")
        return os.getenv(env_key, "")
    return value


def main():
    config = load_config()
    storage_type = config.get("storage_type")

    print(f"Поточний режим запису (з конфігу): {storage_type.upper()}")

    data_file = config.get("data_file", "data.csv")
    data = DataReader.read_csv(data_file)

    if not data:
        print("Немає даних для запису. Зупинка.")
        return

    strategy = None

    if storage_type == "console":
        strategy = ConsoleStrategy()

    elif storage_type == "redis":
        strategy = RedisStrategy(
            host=config["redis"]["host"],
            port=config["redis"]["port"]
        )

    elif storage_type == "kafka":
        strategy = KafkaStrategy(
            bootstrap_servers=config["kafka"]["bootstrap_servers"],
            topic=config["kafka"]["topic"]
        )

    elif storage_type == "firestore":
        f_config = config["firestore"]
        strategy = FirestoreStrategy(
            key_path=resolve_env_variable(f_config["service_account_file"]),
            project_id=resolve_env_variable(f_config["project_id"]),
            collection_name=resolve_env_variable(f_config["collection_name"])
        )

    else:
        print(f"Помилка: Невідомий тип сховища '{storage_type}'")
        return

    strategy.write(data)


if __name__ == "__main__":
    main()