from Entity import Entity
class RentalFee(Entity):
    ENTITY_TYPE = "rentals_fees"
    """Represent a RentalFee element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/rentals_fees/
    """
    def __init__(self,id = None):
        return super(RentalFee,self).__init__("rentals_fees",id)
