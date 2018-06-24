from Entity import Entity


class RentalAmenity(Entity):
    ENTITY_TYPE = "rentals_amenities"
    """Represent a Rental Amenitie element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/rentals_amenities/
    """
    def __init__(self, id=None):
        return super(RentalAmenity, self).__init__("rentals_amenities", id)
