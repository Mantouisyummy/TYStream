class OauthException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NoResultException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)