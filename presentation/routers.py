import os
from fastapi import APIRouter, Depends, HTTPException
from business.services import SteamPlatformService
from business.dependencies import get_platform_service

router = APIRouter(prefix="/platform", tags=["Platform Data Operations"])

@router.post("/load-csv")
def load_csv_data(
    # Впроваджуємо сервіс бізнес-логіки через DI
    service: SteamPlatformService = Depends(get_platform_service)
):
    """
    Ендпоінт презентаційного рівня. Не містить логіки парсингу чи запису,
    лише делегує виклик рівню бізнес-логіки.
    """
    # Будуємо абсолютний шлях до згенерованого файлу data/platform_data.csv
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "platform_data.csv")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="CSV файл не знайдено. Згенеруйте його спочатку.")

    try:
        # Виклик бізнес-логіки
        rows_processed = service.process_and_save_csv_data(file_path)
        return {
            "status": "success",
            "message": "Дані успішно завантажено в БД",
            "rows_processed": rows_processed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка обробки: {str(e)}")

@router.get("/users")
def get_users(service: SteamPlatformService = Depends(get_platform_service)):
    """Допоміжний ендпоінт для перевірки, чи дані збереглися в БД."""
    users = service.repository.get_all_users()
    return {
        "total_users": len(users),
        "sample_users": [{"id": u.userId, "name": u.name} for u in users[:5]]
    }