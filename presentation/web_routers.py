from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# Імпортуємо наш сервіс та DI-залежність
from business.services import SteamPlatformService
from business.dependencies import get_platform_service

# Створюємо роутер для веб-сторінок
router = APIRouter()

# Вказуємо FastAPI, де лежать наші HTML-шаблони
templates = Jinja2Templates(directory="templates")


# ==========================================
# C - Controller: Відображення каталогу ігор
# ==========================================
@router.get("/games", response_class=HTMLResponse)
def list_games(
        request: Request,
        service: SteamPlatformService = Depends(get_platform_service)
):
    # 1. Звертаємось до Моделі (через бізнес-логіку) за даними
    games_from_db = service.get_all_games()

    # 2. Передаємо ці дані у Представлення (View)
    return templates.TemplateResponse(
        request=request,
        name="games_list.html",
        context={"request": request, "games": games_from_db}
    )


# ==========================================
# Показати форму створення гри (GET)
# ==========================================
@router.get("/games/new", response_class=HTMLResponse)
def new_game_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="game_form.html",
        context={"request": request}
    )


# ==========================================
# Прийняти дані з форми і зберегти в БД (POST)
# ==========================================
@router.post("/games/new", response_class=HTMLResponse)
def create_game(
        request: Request,
        title: str = Form(...),  # FastAPI автоматично витягне ці дані з HTML-форми
        genre: str = Form(...),
        service: SteamPlatformService = Depends(get_platform_service)
):
    # Викликаємо бізнес-логіку для збереження
    service.create_game(title, genre)

    # Перенаправляємо користувача назад на головну сторінку з кодом 303 (See Other)
    return RedirectResponse(url="/games", status_code=status.HTTP_303_SEE_OTHER)

# ==========================================
# D - Delete: Видалити гру (POST)
# ==========================================
@router.post("/games/delete/{game_id}", response_class=HTMLResponse)
def delete_game(
    game_id: int,
    service: SteamPlatformService = Depends(get_platform_service)
):
    service.delete_game(game_id)
    # Після видалення просто повертаємо користувача на таблицю
    return RedirectResponse(url="/games", status_code=status.HTTP_303_SEE_OTHER)

# ==========================================
# U - Update: Показати форму редагування (GET)
# ==========================================
@router.get("/games/edit/{game_id}", response_class=HTMLResponse)
def edit_game_form(
    request: Request,
    game_id: int,
    service: SteamPlatformService = Depends(get_platform_service)
):
    # Дістаємо гру з бази, щоб заповнити поля форми старими даними
    game = service.get_game_by_id(game_id)
    return templates.TemplateResponse(
        request=request,
        name="game_edit.html",
        context={"request": request, "game": game}
    )

# ==========================================
# U - Update: Зберегти відредаговану гру (POST)
# ==========================================
@router.post("/games/edit/{game_id}", response_class=HTMLResponse)
def update_game(
    request: Request,
    game_id: int,
    title: str = Form(...),
    genre: str = Form(...),
    service: SteamPlatformService = Depends(get_platform_service)
):
    service.update_game(game_id, title, genre)
    return RedirectResponse(url="/games", status_code=status.HTTP_303_SEE_OTHER)