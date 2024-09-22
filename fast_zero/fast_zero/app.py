from fastapi import FastAPI
from starlette.responses import HTMLResponse

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olá, mundo!'}


@app.get('/ola-mundo', response_class=HTMLResponse)
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
