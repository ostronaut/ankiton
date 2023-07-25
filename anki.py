import os
import requests
import base64


class Anki:
    URL = "http://localhost:8765"

    @staticmethod
    def upload(action: str, **params):
        return requests.post(Anki.URL, json={"action": action, "params": params}).json()

    @staticmethod
    def upload_media_file(path: str):
        with open(path, "rb") as file:
            media_data = base64.b64encode(file.read()).decode("utf-8")

        return Anki.upload(
            "storeMediaFile", filename=os.path.basename(path), data=media_data
        )
