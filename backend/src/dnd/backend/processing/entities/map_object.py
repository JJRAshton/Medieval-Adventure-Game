from .health_entity import HealthEntity


class Object(HealthEntity):

    def __init__(self, objectName: str):
        super().__init__(objectName)
