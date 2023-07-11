from requests.exceptions import RequestException


class MockedResponse:
    def __init__(
        self,
        json_data: dict,
        status_code: int = 200,
        raise_error: bool = False,
    ):
        self.json_data = json_data
        self.status_code = status_code
        self.raise_error = raise_error

    def json(self) -> dict:
        return self.json_data

    def raise_for_status(self):
        if self.raise_error:
            raise RequestException

    @property
    def ok(self):
        return str(self.status_code).startswith("2")
