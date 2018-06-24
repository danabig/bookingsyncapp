from Entity import Entity
from Booking import Booking
class Rental(Entity):
    ENTITY_TYPE = "rentals"
    """Represent a Rental element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/rentals/
    """
    def __init__(self,id = None):
        return super(Rental,self).__init__("rentals",id)
