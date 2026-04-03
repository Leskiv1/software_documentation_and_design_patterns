import csv
import random
from faker import Faker

fake = Faker()


def generate_data(filename: str, num_rows: int = 1050):
    genres = ['RPG', 'Shooter', 'Strategy', 'Simulation', 'Action']
    game_types = ['mmo', 'singleplayer']

    # Згенеруємо невеликий пул ігор та юзерів, щоб вони повторювалися в сесіях
    users_pool = [(fake.user_name(), fake.password()) for _ in range(100)]
    games_pool = [(fake.catch_phrase(), random.choice(genres), fake.company(), random.choice(game_types)) for _ in
                  range(50)]

    print(f"Генерація {num_rows} рядків у файл {filename}...")

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Заголовки (всі сутності в одному рядку)
        writer.writerow([
            'user_name', 'user_password',
            'game_title', 'game_genre', 'game_developer', 'game_type',
            'session_level', 'session_playtime', 'session_is_completed',
            'achievement_list', 'achievement_points'
        ])

        for _ in range(num_rows):
            user = random.choice(users_pool)
            game = random.choice(games_pool)

            writer.writerow([
                user[0], user[1],  # Користувач
                game[0], game[1], game[2], game[3],  # Гра
                f"Level {random.randint(1, 60)}", random.randint(10, 5000),  # Сеанс
                random.choice(['True', 'False']),
                f"Achiev_{random.randint(1, 100)}", random.randint(10, 500)  # Досягнення
            ])

    print("Генерацію завершено!")


if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')

    os.makedirs(data_dir, exist_ok=True)
    generate_data(os.path.join(data_dir, 'platform_data.csv'), 1050)