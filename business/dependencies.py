from fastapi import Depends
from sqlalchemy.orm import Session
from data_access.database import get_db
from data_access.interfaces import IDataLoader, IPlatformRepository
from data_access.csv_reader import CSVDataLoader
from data_access.repositories import SQLitePlatformRepository
from business.services import SteamPlatformService

# Провайдер для читача даних (повертає конкретний CSV-рідер під виглядом інтерфейсу)
def get_data_loader() -> IDataLoader:
    return CSVDataLoader()

# Провайдер для репозиторію (автоматично отримує сесію БД і передає в репозиторій)
def get_repository(db: Session = Depends(get_db)) -> IPlatformRepository:
    return SQLitePlatformRepository(db)

# Головний провайдер для сервісу бізнес-логіки
def get_platform_service(
    data_loader: IDataLoader = Depends(get_data_loader),
    repository: IPlatformRepository = Depends(get_repository)
) -> SteamPlatformService:
    # FastAPI сам створить data_loader та repository і передасть їх сюди
    return SteamPlatformService(data_loader, repository)