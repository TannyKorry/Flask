from typing import Type, Union

from flask import Flask, jsonify, request
from flask.views import MethodView
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from schema import CreateAds
from models import Session, ADS

app = Flask("app")


# В случае возникновинии определенных ошибок прекратить выполнять вьюху, выполнить заданную логику и возвратить клиенту что-то на базе этой логики
class HttpError(Exception):
    def __init__(self, status_code: int, error_message: Union[dict, list, str]):
        self.status_code = status_code
        self.error_message = error_message


# функция, которая будет выполняться в случае возникновения ошибки
@app.errorhandler(HttpError)
def error_handler(er: HttpError):
    http_response = jsonify({"status": "error", "description": er.error_message})
    http_response.status_code = er.status_code
    return http_response


def validate(schema, json_data: dict):
    try:
        model = schema(**json_data)
        validated_data = model.dict(exclude_none=True)
    except ValidationError as er:
        raise HttpError(400, er.errors())
    return validated_data


# функция выбросит 404, если не найдется объявление с таким id
def get_ad_valid(session: Session, ads_id: int):
    ad = session.get(ADS, ads_id)
    if ad is None:
        raise HttpError(404, "ads_id not found")
    return ad


class AdsView(MethodView):

    def get(self, ads_id: int):
        with Session() as session:
            ad = get_ad_valid(session, ads_id)
        return jsonify(
            {"id": ad.id, "title": ad.title, "text": ad.text, "user": ad.user,
                "published_at": ad.published_at.isoformat(),
            }
        )

    def post(self):
        json_data = validate(CreateAds, request.json)
        with Session() as session:
            ad = ADS(**json_data)
            session.add(ad)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "advertisement already exists")
            return jsonify({"status": "success", "id": ad.id})

    def delete(self, ads_id: int):
        with Session() as session:
            ad = get_ad_valid(session, ads_id)
            session.delete(ad)
            session.commit()
            return jsonify({"status": "success", "id": ads_id})


ads_view = AdsView.as_view("advertisements")


app.add_url_rule("/ads/<int:ads_id>", view_func=ads_view, methods=["GET", "DELETE"])
app.add_url_rule("/ads/", view_func=ads_view, methods=["POST"])


if __name__ == "__main__":
    app.run()
