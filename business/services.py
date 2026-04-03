from data_access.interfaces import IDataLoader, IPlatformRepository
from data_access.models import User, Game, GameSession, Achievement


class SteamPlatformService:
    # Впровадження залежностей (Dependency Injection) через конструктор
    def __init__(self, data_loader: IDataLoader, repository: IPlatformRepository):
        self.data_loader = data_loader
        self.repository = repository

    def process_and_save_csv_data(self, file_path: str):
        """Головна бізнес-логіка: зчитування, мапінг моделей, збереження."""
        # 1. Вичитування даних з файлу
        raw_data = self.data_loader.read_data(file_path)

        # Використовуємо словники для уникнення дублікатів (оскільки CSV денормалізований)
        unique_users = {}
        unique_games = {}

        sessions_to_save = []
        achievements_to_save = []

        # 2. Створення необхідних моделей для заповнення бази даних
        for row in raw_data:
            # Парсимо Користувача
            username = row['user_name']
            if username not in unique_users:
                unique_users[username] = User(name=username, password=row['user_password'])

            # Парсимо Гру
            game_title = row['game_title']
            if game_title not in unique_games:
                unique_games[game_title] = Game(
                    title=game_title,
                    genre=row['game_genre'],
                    developer=row['game_developer'],
                    game_type=row['game_type']
                )

            # Парсимо Сеанс (пов'язуємо з об'єктами юзера та гри)
            session = GameSession(
                user=unique_users[username],
                game=unique_games[game_title],
                currentLevel=row['session_level'],
                playtime=int(row['session_playtime']),
                isCompleted=row['session_is_completed'].lower() == 'true'
            )
            sessions_to_save.append(session)

            # Парсимо Досягнення
            achievement = Achievement(
                game=unique_games[game_title],
                achievementList=row['achievement_list'],
                totalPoints=int(row['achievement_points'])
            )
            achievements_to_save.append(achievement)

        # 3. Виклик рівня доступу до даних для збереження інформації
        self.repository.save_parsed_data(
            users=list(unique_users.values()),
            games=list(unique_games.values()),
            sessions=sessions_to_save,
            achievements=achievements_to_save
        )

        return len(raw_data)  # Повертаємо кількість оброблених рядків

    def get_all_games(self):
        return self.repository.get_all_games()

    def get_game_by_id(self, game_id: int):
        return self.repository.get_game_by_id(game_id)

    def create_game(self, title: str, genre: str):
        return self.repository.create_game(title, genre)

    def update_game(self, game_id: int, title: str, genre: str):
        return self.repository.update_game(game_id, title, genre)

    def delete_game(self, game_id: int):
        return self.repository.delete_game(game_id)