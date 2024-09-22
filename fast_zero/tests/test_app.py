from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá, mundo!'}


def test_read_ola_mundo_deve_retornar_ok_e_html(client):
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


def test_create_user_deve_retornar_created_nome_e_email(client):
    response = client.post(
        '/users',
        json={
            'id': 0,
            'name': 'string',
            'email': 'user@example.com',
            'password': 'string',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'name': 'string',
        'email': 'user@example.com',
        'id': 1,
    }


def test_read_user_deve_retornar_ok_e_lista_de_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'name': 'string',
                'email': 'user@example.com',
                'id': 1,
            }
        ]
    }


def test_update_user_deve_retornar_ok_nome_email_e_id(client):
    response = client.put(
        '/users/1',
        json={
            'name': 'patrick',
            'email': 'patrick@ribeiro.com',
            'password': 'novasenha',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': 'patrick',
        'email': 'patrick@ribeiro.com',
        'id': 1,
    }


def test_update_user_deve_retornar_not_found_e_mensagem_not_found(client):
    response = client.put(
        '/users/0',
        json={
            'name': 'patrick',
            'email': 'patrick@ribeiro.com',
            'password': 'novasenha',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found.'}


def test_read_user_by_id_deve_retornar_ok_nome_email_e_id(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': 'patrick',
        'email': 'patrick@ribeiro.com',
        'id': 1,
    }


def test_read_user_by_id_deve_retornar_not_found_e_detail_not_found(client):
    response = client.get('/users/0')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found.'}


def test_delete_user_deve_retornar_ok_e_mensagem_user_deleted(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted.'}


def test_delete_user_deve_retornar_not_found_e_detail_user_not_found(client):
    response = client.delete('/users/0')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found.'}
