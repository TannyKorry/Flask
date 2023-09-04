from hashlib import md5
from typing import Type

from flask import Flask, jsonify, request
from flask.views import MethodView
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from schema import CreateUser, UpdateUser
from models import Session, User

app = Flask('app')

# Преобразование пароля
SALT = "fxc vbnkiui7yu6trfd"
def hash_password(password: str):
    password = f"{SALT}{password}"
    password = password.encode()
    return md5(password).hexdigest()


class HttpError(Exception):
    def __init__(self, status_code: int, error_message: dict | list | str):
        self.status_code = status_code
        self.error_message = error_message


@app.errorhandler(HttpError)
def error_handler(er: HttpError):
    http_response = jsonify({"status": "error", "description": er.error_message})
    http_response.status_code = er.status_code
    return http_response


def validate(schema: Type[CreateUser] | Type[UpdateUser], json_data: dict):
    try:
        model = schema(**json_data)
        validated_data = model.dict(exclude_none=True)
    except ValidationError as er:
        raise HttpError(400, er.errors())
    return validated_data


def get_user(session: Session, user_id: int):
    user = session.get(User, user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user


class UserView(MethodView):
    
    def get(self, user_id: int):
        with Session() as session:
            user = get_user(session, user_id)
        return jsonify(
            {
                'id': user.id,
                'name': user.name,
                'creation_time': user.creation_time.isoformat(),
            }
        )


    def post(self):
        json_data = validate(CreateUser, request.json)
        json_data["password"] = hash_password(json_data["password"])

        with Session() as session:
            user = User(**json_data)
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "user already exists")
            return jsonify({"status": "success", "id": user.id})

    def patch(self, user_id: int):
        json_data = validate(UpdateUser, request.json)
        if 'password' in json_data:
            json_data['password'] = hash_password(json_data['password'])
        with Session() as session:
            user = get_user(session, user_id)
            for field, value in json_data.items():
                setattr(user, field, value)
            session.add(user)
            session.commit()
            return jsonify({"status": "success", "id": user.id})

    def delete(self, user_id: int):
        with Session() as session:
            user = get_user(session, user_id)
            session.delete(user)
            session.commit()
            return jsonify({"status": "success", "id": user_id})
     
user_view = UserView.as_view('users')



app.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users/', view_func=user_view, methods=['POST'])



if __name__ == '__main__':
    app.run()
