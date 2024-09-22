from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá, mundo!'}


def test_read_ola_mundo_deve_retornar_ok_e_html():
    client = TestClient(app)
    response = client.get('/ola-mundo')
    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
    <html>
        <head>
            <title>
                My hello world
            </title>
        </head>
        <body>
            <h1>
                Helo, World, from Patrick!
            </h1>
        </body>
    </html>"""
    )
