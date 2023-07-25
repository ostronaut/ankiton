import requests
import backoff


class URLRequest:
    def __init__(self, url: str) -> None:
        self._url = url

    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.RequestException,
        max_tries=3,
        factor=1.5,
        max_time=10,
        jitter=backoff.full_jitter,
    )
    def request(self) -> requests.Response:
        response = requests.get(self._url)
        response.raise_for_status()
        return response

    def request_save_mp3(self, file: str) -> None:
        response = self.request()
        
        with open(file, "wb") as f:
            f.write(response.content)
