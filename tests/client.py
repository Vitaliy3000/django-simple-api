import requests


class ClientFactory:
    def __init__(self, url):
        self._url = url

    def create_client(self):
        return Client(url=self._url)


class Client:
    def __init__(self, url):
        self._url = url
        self._headers = {
            "Content-Type": "application/json",
        }
        self._access_token = None
        self._refresh_token = None
        self.is_authenticated = False

    def authenticate(self, email, password):
        data = requests.post(
            f"{self._url}token/", json={"email": email, "password": password}
        ).json()

        self._access_token = data["access"]
        self._refresh_token = data["refresh"]
        self._headers["Authorization"] = f"Bearer {self._access_token}"
        self.is_authenticated = True

    def list_users(self):
        return requests.get(f"{self._url}users/", headers=self._headers)

    def create_user(self, email, password):
        return requests.post(
            f"{self._url}users/",
            headers=self._headers,
            json={"email": email, "password": password},
        )

    def delete_user(self, user_id):
        return requests.delete(f"{self._url}users/{user_id}/", headers=self._headers)

    def list_resources(self, user_id=None):
        resource_url = self.get_resource_url(user_id)
        return requests.get(resource_url, headers=self._headers)

    def create_resource(self, resource_name, user_id=None):
        resource_url = self.get_resource_url(user_id)
        return requests.post(
            resource_url,
            headers=self._headers,
            json={"name": resource_name},
        )

    def delete_resource(self, resource_id, user_id=None):
        resource_url = self.get_resource_url(user_id)
        return requests.delete(
            f"{resource_url}{resource_id}/",
            headers=self._headers,
        )

    def get_resource_url(self, user_id=None):
        if user_id is None:
            return f"{self._url}users/resources/"
        else:
            return f"{self._url}users/{user_id}/resources/"

    def set_quota(self, user_id, quota):
        return requests.patch(
            f"{self._url}users/{user_id}/quota/",
            headers=self._headers,
            json={"quota": quota},
        )
