import json
from urllib.parse import urlencode
from urllib.request import urlopen


class GeoNamesClient:
    """Generic client for GeoNames endpoints.

    Example:
        client = GeoNamesClient(endpoint="hierarchyJSON", username="robert")
        data = client.get({"geonameId": 2759794})
    """

    def __init__(
        self,
        endpoint,
        username="robert",
        base_url="http://api.geonames.org",
        timeout=30,
    ):
        self.base_url = base_url.rstrip("/")
        self.endpoint = endpoint.lstrip("/")
        self.username = username
        self.timeout = timeout

    @property
    def url(self):
        return f"{self.base_url}/{self.endpoint}"

    def get(self, params=None):
        """Perform a GET request and return decoded JSON."""
        params = dict(params or {})
        params.setdefault("username", self.username)

        query = urlencode(params)
        request_url = f"{self.url}?{query}"

        with urlopen(request_url, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))


def get_hierarchy_chain(geoname_id, username="robert"):
    """Backward-compatible helper for the hierarchy endpoint."""
    client = GeoNamesClient(endpoint="hierarchyJSON", username=username)
    return client.get({"geonameId": geoname_id})