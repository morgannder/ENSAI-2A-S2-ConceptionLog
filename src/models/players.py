class Player:
    def __init__(self, id: int, platform_id: int, platform_user_id: str, name: str):
        self._id = id
        self._platform_id = platform_id
        self._platform_usbiginter_id = platform_user_id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def platform_id(self):
        return self._platform_id

    @property
    def platform_user_id(self):
        return self._platform_user_id

    @property
    def name(self):
        return self._name
