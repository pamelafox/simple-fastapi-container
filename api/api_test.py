import random

from . import create_app

app = create_app()


def test_generate_name():
    random.seed(1)
    response = app.test_client().get("/generate_name")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Belton"


def test_generate_name_params():
    random.seed(1)
    response = app.test_client().get("/generate_name?starts_with=n")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Nancy"


def test_generate_name_params_upper():
    random.seed(1)
    response = app.test_client().get("/generate_name?starts_with=NE")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Newell"
