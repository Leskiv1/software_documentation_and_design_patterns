from sqlalchemy.orm import Session
from data_access.interfaces import IPlatformRepository
from data_access.models import User


class SQLitePlatformRepository(IPlatformRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def save_parsed_data(self, users: list, games: list, sessions: list, achievements: list) -> None:
        """Зберігає всі підготовлені об'єкти в базу даних за одну транзакцію."""
        self.db.add_all(users)
        self.db.add_all(games)
        self.db.flush()  # Отримуємо ID для ігор та юзерів перед збереженням сесій

        self.db.add_all(sessions)
        self.db.add_all(achievements)
        self.db.commit()  # Фіксуємо зміни в БД

    def get_all_users(self) -> list:
        return self.db.query(User).all()