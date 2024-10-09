from http import HTTPStatus

from fast_zero.schemas import UserPublic


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
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_user_deve_retornar_ok_e_lista_de_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users_deve_retornar_ok_e_lista_de_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.json() == {'users': [user_schema]}


def test_update_user_deve_retornar_ok_nome_email_e_id(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'patrick',
            'email': 'patrick@ribeiro.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'patrick',
        'email': 'patrick@ribeiro.com',
        'id': 1,
    }


def test_update_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'newuser',
            'email': 'newuser@teste.com',
            'password': 'senhateste',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'newuser',
            'email': 'teste@test.com',
            'password': 'senhateste',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists.'}


def test_update_user_deve_retornar_not_found_e_mensagem_not_found(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'patrick',
            'email': 'patrick@ribeiro.com',
            'password': 'novasenha',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found.'}


def test_read_user_by_id_deve_retornar_ok_nome_email_e_id(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_user_by_id_deve_retornar_not_found_e_detail_not_found(client):
    response = client.get('/users/0')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found.'}


def test_delete_user_deve_retornar_ok_e_mensagem_user_deleted(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted.'}


def test_delete_user_deve_retornar_not_found_e_detail_user_not_found(client):
    response = client.delete('/users/0')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found.'}


def test_create_user_which_username_and_email_already_exist(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'teste',
            'email': 'teste@test.com',
            'password': 'mypassword',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username and email already exist.'}


def test_create_user_which_username_already_exists(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'teste',
            'email': 'teste@teste.com',
            'password': 'mypassword',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists.'}


def test_create_user_which_email_already_exists(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'novoteste',
            'email': 'teste@test.com',
            'password': 'mypassword',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists.'}
