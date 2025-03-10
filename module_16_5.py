# Домашнее задание по теме "Шаблонизатор Jinja 2."
# Если вы решали старую версию задачи, проверка будет производиться по ней.
# Ссылка на старую версию тут.
#
# Цель: научиться взаимодействовать с шаблонами Jinja 2 и использовать их в запросах.
#
# Задача "Список пользователей в шаблоне":
# Подготовка:
# Используйте код из предыдущей задачи.
# Скачайте заготовленные шаблоны для их дополнения.
# Шаблоны оставьте в папке templates у себя в проекте.
# Создайте объект Jinja2Templates, указав в качестве папки шаблонов - templates.
# Измените и дополните ранее описанные CRUD запросы:
# Напишите новый запрос по маршруту '/':
# Функция по этому запросу должна принимать аргумент request и возвращать TemplateResponse.
# TemplateResponse должен подключать ранее заготовленный шаблон 'users.html', а также передавать в него request и список users. Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.
# Измените get запрос по маршруту '/user' на '/user/{user_id}':
# Функция по этому запросу теперь принимает аргумент request и user_id.
# Вместо возврата объекта модели User, теперь возвращается объект TemplateResponse.
# TemplateResponse должен подключать ранее заготовленный шаблон 'users.html', а также передавать в него request и одного из пользователей - user. Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.
# Создайте несколько пользователей при помощи post запроса со следующими данными:
# username - UrbanUser, age - 24
# username - UrbanTest, age - 22
# username - Capybara, age - 60
# В шаблоне 'users.html' заготовлены все необходимые теги и обработка условий, вам остаётся только дополнить закомментированные строки вашим Jinja 2 кодом (использование полей id, username и age объектов модели User):
# 1. По маршруту '/' должен отображаться шаблон 'users.html' со списком все ранее созданных объектов:
#
# 2. Здесь каждая из записей является ссылкой на описание объекта, информация о котором отображается по маршруту '/user/{user_id}':
#
#
# Так должен выглядеть Swagger:
#
#
# Иерархия в проекте:
#
#
# Примечания:
# Основные теги HTML.
from http.client import HTTPResponse

# uvicorn module_16_5:app --reload
# http://127.0.0.1:8000/docs


from fastapi import FastAPI, Request, HTTPException, Path, Form
from fastapi.responses import  HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
class User(BaseModel):
    id: int
    username: str
    age: int

class UserPost(BaseModel):
    username: str
    age: int

users: List[User] = []

# swagger_ui_parameters={"tryItOutEnabled": True} - активировать кнопку
app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_user(
        request: Request,
        user_id: Annotated[int, Path(ge=1)]):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="Пользователь не найден")


'''
@app.post("/user/{username}/{age}", response_class=HTMLResponse)
async def post_user(
        request: Request,
        username: Annotated[str, Path(min_length=3, max_length=50, patern="^[a-zA-Z_-]", description="Enter Username",
                                      examples='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, title="User age", description="Enter age", examples="24")])->HTMLResponse:
    new_id = max((user.id for user in users), default=0) + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})
'''
@app.post("/user", response_class=HTMLResponse)
async def post_user(request: Request, username: str = Form(), age: int = Form() ):
    new_id = max((user.id for user in users), default=0) + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.put("/user/{user_id}/{username}/{age}", response_class=HTMLResponse)
async def update_user(
        request: Request,
        user_id: Annotated[int, Path(ge=1, description="Enter User ID", examples='1')],
        username: Annotated[str, Path(min_length=3, max_length=50, patern="^[a-zA-Z_-]", description="Enter Username",
                                      examples='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, title="User age", description="Enter age", examples="24")]):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail='Пользователь не найден')

@app.delete("/user/{user_id}", response_class=HTMLResponse)
async def delete_user(
        request: Request,
        user_id: Annotated[int, Path(ge=1, description="Enter User ID", examples='1')]):
    for i, user in enumerate(users):
        if user.id == user_id:
            del users[i]
            return templates.TemplateResponse("users.html", {"request": request, "users": users})
    raise HTTPException(status_code=404, detail='Пользователь не найден')
