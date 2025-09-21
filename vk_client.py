import requests
from typing import Dict, Any, List

from config import VK_API_VERSION, ACCESS_TOKEN


class VKClient:
    """Клиент для работы с VK API."""

    def __init__(self, token: str = ACCESS_TOKEN, version: str = VK_API_VERSION):
        self.base_url = "https://api.vk.com/method/"
        self.token = token
        self.version = version

    def _request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        params.update({
            "access_token": self.token,
            "v": self.version,
        })
        response = requests.get(f"{self.base_url}{method}", params=params)
        data = response.json()
        if "error" in data:
            raise Exception(f"VK API error: {data['error']}")
        return data["response"]

    def get_users_by_city(self, city_id: int, count: int = 50) -> List[Dict[str, Any]]:
        return self._request("users.search", {
            "city": city_id,
            "count": count,
            "has_photo": 1,
            "fields": "photo_max_orig"
        })["items"]

    def get_photos(self, owner_id: int, count: int = 50) -> List[Dict[str, Any]]:
        return self._request("photos.getAll", {
            "owner_id": owner_id,
            "count": count,
            "photo_sizes": 1
        })["items"]
