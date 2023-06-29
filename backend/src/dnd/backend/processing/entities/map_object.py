from .stats.assign_entity import EntityFactory
from .health_entity import HealthEntity


class Object(HealthEntity):

    entityStats = EntityFactory()

    def __init__(self, objectName: str):
        super().__init__(objectName)

        self.getStats()
        self.reset_health()
        self.resetSize()

    def getStats(self):
        Object.entityStats.getObjectStats(self)
