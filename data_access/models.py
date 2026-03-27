from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    userId = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    # Зв'язок 1 до багатьох (один користувач має багато сеансів)
    sessions = relationship("GameSession", back_populates="user")


class Game(Base):
    __tablename__ = 'games'

    gameId = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    genre = Column(String, nullable=False)
    developer = Column(String, nullable=False)

    # Поля для дочірніх класів з UML (MMO та Одиночна) - для простоти в одній таблиці
    game_type = Column(String)  # 'mmo' або 'singleplayer'
    serverUrl = Column(String, nullable=True)
    difficulty = Column(String, nullable=True)

    sessions = relationship("GameSession", back_populates="game")
    achievements = relationship("Achievement", back_populates="game")


class GameSession(Base):
    __tablename__ = 'game_sessions'

    sessionId = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('users.userId'))
    gameId = Column(Integer, ForeignKey('games.gameId'))
    currentLevel = Column(String)
    playtime = Column(Integer)
    isCompleted = Column(Boolean, default=False)

    user = relationship("User", back_populates="sessions")
    game = relationship("Game", back_populates="sessions")


class Achievement(Base):
    __tablename__ = 'achievements'

    achievementId = Column(Integer, primary_key=True, index=True)
    gameId = Column(Integer, ForeignKey('games.gameId'))
    achievementList = Column(String)  # Можна зберігати як JSON-рядок або просто текст
    totalPoints = Column(Integer)

    game = relationship("Game", back_populates="achievements")