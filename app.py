import requests
from flask import Flask

app = Flask(__name__)


class GithubUser:
    def __init__(self, username, profile_url, public_repos, followers, following):
        self.username = username
        self.profile_url = profile_url
        self.public_repos = public_repos
        self.followers = followers
        self.following = following

    def __repr__(self):
        return f"GithubUser('{self.username}', '{self.profile_url}', {self.public_repos}, {self.followers}, {self.following})"

    @staticmethod
    def from_username(username):
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            user = GithubUser(
                data['login'],
                data['html_url'],
                data['public_repos'],
                data['followers'],
                data['following']
            )
            return user
        else:
            raise ValueError(
                "Usuário não encontrado. Certifique-se de ter digitado o username correto e tente novamente.")

    def get_repo_dict(self):
        url = f"https://api.github.com/users/{self.username}/repos"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            repo_dict = {}
            for repo in data:
                repo_dict[repo['name']] = repo['html_url']
            return repo_dict
        else:
            return "Erro ao obter repositórios.", 400

    def generate_txt_file(self):
        repo_dict = self.get_repo_dict()

        with open(f"{self.username}.txt", "w") as file:
            file.write(f"Nome do usuário: {self.username}\n")
            file.write(f"URL do perfil: {self.profile_url}\n")
            file.write(f"Número de repositórios públicos: {self.public_repos}\n")
            file.write(f"Número de seguidores: {self.followers}\n")
            file.write(f"Número de pessoas que segue: {self.following}\n\n")
            file.write("Repositórios:\n")
            for name, url in repo_dict.items():
                file.write(f"{name}: {url}\n")

        return f"Arquivo gerado: {self.username}.txt"

@app.route('/github_user/<username>')
def get_github_user(username):
    try:
        user = GithubUser.from_username(username)
        user.generate_txt_file()
        return {'message': f'As informações do usuário {username} foram geradas no arquivo txt.'}
    except ValueError as e:
        return str(e), 400


if __name__ == '__main__':
    app.run(debug=True)
