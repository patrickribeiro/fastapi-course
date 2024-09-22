from http import HTTPStatus

from fastapi import FastAPI
from starlette.responses import HTMLResponse

from fast_zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá, mundo!'}


@app.get('/ola-mundo', response_class=HTMLResponse, status_code=HTTPStatus.OK)
def ola_mundo():
    return """
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
