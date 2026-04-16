from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IDataLoader(ABC):
    """Інтерфейс для зчитування сирих даних (наприклад, з CSV)."""

    @abstractmethod
    def read_data(self, file_path: str) -> List[Dict[str, Any]]:
        pass


class IPlatformRepository(ABC):
    """Інтерфейс для роботи з базою даних."""

    @abstractmethod
    def save_parsed_data(self, users: list, games: list, sessions: list, achievements: list) -> None:
        """Зберігає всі розпарсені сутності в базу даних."""
        pass

    @abstractmethod
    def get_all_users(self) -> list:
        pass

    @abstractmethod
    def get_all_games(self):
        pass

    @abstractmethod
    def get_game_by_id(self, game_id: int):
        pass

    @abstractmethod
    def create_game(self, title: str, genre: str):
        pass

    @abstractmethod
    def update_game(self, game_id: int, title: str, genre: str):
        pass

    @abstractmethod
    def delete_game(self, game_id: int):
        pass