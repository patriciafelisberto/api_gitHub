import os
import pytest
import json
from app import GithubUser, app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_githubUser_from_username():
    # Testa se a classe GithubUser pode obter informações de um usuário existente
    user = GithubUser.from_username("octocat")
    assert user.username == "octocat"
    assert user.public_repos == 8


def test_githubUser_from_username_not_found():
    # Testa se a classe GithubUser retorna um ValueError quando o usuário não existe
    with pytest.raises(ValueError):
        GithubUser.from_username("usuario_inexistente")


def test_githubUser_generate_txt_file():
    # Testa se a classe GithubUser pode gerar um arquivo txt
    user = GithubUser.from_username("octocat")
    result = user.generate_txt_file()
    assert os.path.exists("octocat.txt")
    assert result == "Arquivo gerado: octocat.txt"


def test_get_github_user(client):
    # Testa se a função get_github_user retorna uma resposta válida para um usuário existente
    response = client.get('/github_user/octocat')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["message"] == "As informações do usuário octocat foram geradas no arquivo txt."



def test_get_github_user_not_found(client):
    # Testa se a função get_github_user retorna um erro 400 para um usuário inexistente
    response = client.get('/github_user/usuario_inexistente')
    assert response.status_code == 400
    assert "Usuário não encontrado".encode() in response.data


