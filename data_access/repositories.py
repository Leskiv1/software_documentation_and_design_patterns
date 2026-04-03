from sqlalchemy.orm import Session
from data_access.interfaces import IPlatformRepository
from data_access.models import User, Game


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

    def get_all_games(self):
        return self.db.query(Game).all()

    def get_game_by_id(self, game_id: int):
        return self.db.query(Game).filter(Game.gameId == game_id).first()

    def create_game(self, title: str, genre: str):
        new_game = Game(
            title=title,
            genre=genre,
            developer="Unknown",
            game_type="Standard",
            serverUrl="http://localhost",
            difficulty="Medium"
        )
        self.db.add(new_game)
        self.db.commit()
        return new_game

    def update_game(self, game_id: int, title: str, genre: str):
        game = self.get_game_by_id(game_id)
        if game:
            game.title = title
            game.genre = genre
            self.db.commit()
        return game

    def delete_game(self, game_id: int):
        game = self.get_game_by_id(game_id)
        if game:
            self.db.delete(game)
            self.db.commit()
            return True
        return False