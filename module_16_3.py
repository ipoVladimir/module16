# Домашнее задание по теме "CRUD Запросы: Get, Post, Put Delete."
# Цель: выработать навык работы с CRUD запросами.
#
# Задача "Имитация работы с БД":
# Создайте новое приложение FastAPI и сделайте CRUD запросы.
# Создайте словарь users = {'1': 'Имя: Example, возраст: 18'}
# Реализуйте 4 CRUD запроса:
# get запрос по маршруту '/users', который возвращает словарь users.
# post запрос по маршруту '/user/{username}/{age}', который добавляет в словарь по максимальному по значению ключом значение строки "Имя: {username}, возраст: {age}". И возвращает строку "User <user_id> is registered".
# put запрос по маршруту '/user/{user_id}/{username}/{age}', который обновляет значение из словаря users под ключом user_id на строку "Имя: {username}, возраст: {age}". И возвращает строку "The user <user_id> is updated"
# delete запрос по маршруту '/user/{user_id}', который удаляет из словаря users по ключу user_id пару.
# Выполните каждый из этих запросов по порядку. Ответы должны совпадать:
# 1. GET '/users'
# {
# "1": "Имя: Example, возраст: 18"
# }
# 2. POST '/user/{username}/{age}' # username - UrbanUser, age - 24
# "User 2 is registered"
# 3. POST '/user/{username}/{age}' # username - NewUser, age - 22
# "User 3 is registered"
# 4. PUT '/user/{user_id}/{username}/{age}' # user_id - 1, username - UrbanProfi, age - 28
# "User 1 has been updated"
# 5. DELETE '/user/{user_id}' # user_id - 2
# "User 2 has been deleted"
# 6. GET '/users'
# {
# "1": "Имя: UrbanProfi, возраст: 28",
# "3": "Имя: NewUser, возраст: 22"
# }
# Пример результата выполнения программы:
# Как должен выглядеть Swagger:
#
#
# Примечания:
# Не забудьте написать валидацию для каждого запроса, аналогично предыдущему заданию.

# uvicorn module_16_3:app --reload
# http://127.0.0.1:8000/user/110

from typing import Annotated
from fastapi import FastAPI, Path, HTTPException

users = [
    {'1': 'Имя: Example, возраст: 18'}
]

app = FastAPI()

@app.get("/users")
async def get_users():
    return users

@app.post("/user/{username}/{age}")
async def post_user(
        username: Annotated[str, Path(min_length=3, max_length=50, patern="^[a-zA-Z_-]", description="Enter Username",
                                      examples='UrbanUser')],
        age: Annotated[int, Path(ge=18,le=120, title="User age", description="Enter age", examples="24")]) -> str:
    #new_user_id = max(int(user[0]) for user in users) + 1 if users else 1
    list_user_id = []
    for user in users:
        for k, v in user.items(): pass
        list_user_id.append(int(k))
    new_user_id = max(list_user_id) + 1 if list_user_id else 1
    new_user = {f'{new_user_id}': f'Имя: {username}, возраст: {age}'}
    users.append(new_user)
    return f"User {new_user_id} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: Annotated[int, Path(ge=1, description="Enter User ID", examples='1')],
        username: Annotated[str, Path(min_length=3, max_length=50, patern="^[a-zA-Z_-]", description="Enter Username",
                                      examples='UrbanUser')],
        age: Annotated[int, Path(ge=18,le=120, title="User age", description="Enter age", examples="24")]) -> str:
    for user in users:
        #if int(user.items()[0]) == user_id:
        for k, v in user.items(): pass
        if int(k) == user_id:
            user[k] = f'Имя: {username}, возраст: {age}'
            return f'The user {user_id} is updated'
    raise HTTPException(status_code=404, detail='Пользователь не найден')

@app.delete("/user/{user_id}")
async def delete_user(
        user_id: Annotated[int, Path(ge=1, description="Enter User ID", examples='1')]) -> str:
    for i, user in enumerate(users):
        #if int(user[0]) == user_id:
        for k, v in user.items(): pass
        if int(k) == user_id:
            del users[i]
            return f'User {user_id} has been deleted'
    raise HTTPException(status_code=404, detail='Пользователь не найден')
