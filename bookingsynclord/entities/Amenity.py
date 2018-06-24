from Entity import Entity


class Amenity(Entity):
    ENTITY_TYPE = "amenities"
    """Represent a Rental Amenitie element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/amenities/
    """
    def __init__(self, id=None):
        return super(Amenity, self).__init__("amenities", id)
