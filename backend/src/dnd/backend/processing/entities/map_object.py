from .health_entity import HealthEntity


class Object(HealthEntity):

    def __init__(self, objectName: str, max_health):
        super().__init__(objectName, max_health=max_health)
