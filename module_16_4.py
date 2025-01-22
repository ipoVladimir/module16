# Домашнее задание по теме "Модели данных Pydantic"
# Если вы решали старую версию задачи, проверка будет производиться по ней.
# Ссылка на старую версию тут.
#
# Цель: научиться описывать и использовать Pydantic модель.
#
# Задача "Модель пользователя":
# Подготовка:
# Используйте CRUD запросы из предыдущей задачи.
# Создайте пустой список users = []
# Создайте класс(модель) User, наследованный от BaseModel, который будет содержать следующие поля:
# id - номер пользователя (int)
# username - имя пользователя (str)
# age - возраст пользователя (int)
#
# Измените и дополните ранее описанные 4 CRUD запроса:
# get запрос по маршруту '/users' теперь возвращает список users.
# post запрос по маршруту '/user/{username}/{age}', теперь:
# Добавляет в список users объект User.
# id этого объекта будет на 1 больше, чем у последнего в списке users. Если список users пустой, то 1.
# Все остальные параметры объекта User - переданные в функцию username и age соответственно.
# В конце возвращает созданного пользователя.
# put запрос по маршруту '/user/{user_id}/{username}/{age}' теперь:
# Обновляет username и age пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
# В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием "User was not found" и кодом 404.
# delete запрос по маршруту '/user/{user_id}', теперь:
# Удаляет пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
# В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием "User was not found" и кодом 404.
# Выполните каждый из этих запросов по порядку. Ответы должны совпадать:
# 1. GET '/users'
# []
# 2. POST '/user/{username}/{age}' # username - UrbanUser, age - 24
#
# 3. POST '/user/{username}/{age}' # username - UrbanTest, age - 36
#
# 4. POST '/user/{username}/{age}' # username - Admin, age - 42
#
# 5. PUT '/user/{user_id}/{username}/{age}' # user_id - 1, username - UrbanProfi, age - 28
#
# 6. DELETE '/user/{user_id}' # user_id - 2
#
# 7. GET '/users'
#
# 8. DELETE '/user/{user_id}' # user_id - 2

# uvicorn module_16_4:app --reload
# http://127.0.0.1:8000/docs

from typing import Annotated, List
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    age: int

class UserPost(BaseModel):
    username: str
    age: int

users: List[User] = []

app = FastAPI()

@app.get("/users")
async def get_users():
    return users

@app.post("/user/{username}/{age}", response_model=User)
async def post_user(user: UserPost)->User:
    new_id = max((usr.id for usr in users), default=0) + 1
    new_user = User(id=new_id, username=user.username, age=user.age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(
        user_id: Annotated[int, Path(ge=1, description="Enter User ID", examples='1')],
        user: UserPost):
    for usr in users:
        if usr.id == user_id:
            usr.username = user.username
            usr.age = user.age
            return usr
    raise HTTPException(status_code=404, detail='Пользователь не найден')

@app.delete("/user/{user_id}", response_model=dict)
async def delete_user(
        user_id: Annotated[int, Path(ge=1, description="Enter User ID", examples='1')]):
    for i, user in enumerate(users):
        if user.id == user_id:
            del users[i]
            return {"detail": "Пользователь удален"}
    raise HTTPException(status_code=404, detail='Пользователь не найден')
