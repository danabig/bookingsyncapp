from GenericStore import GenericStore

class NightlyRateMapStore(GenericStore):
    """Store used to manage BookingFee entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/nightly_rate_maps/
    """
    def __init__(self,credential_manager):
        super(NightlyRateMapStore, self).__init__(credential_manager,"nightly_rate_maps")
