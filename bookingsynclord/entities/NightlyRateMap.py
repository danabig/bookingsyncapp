from Entity import Entity
class NightlyRateMap(Entity):
    """Represent a Nightly Rate Map element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/nightly_rate_maps/
    """
    ENTITY_TYPE = "nightly_rate_maps"
    def __init__(self,id = None):
        return super(NightlyRateMap,self).__init__("nightly_rate_maps",id)
