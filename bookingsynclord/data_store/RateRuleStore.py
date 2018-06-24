from GenericStore import GenericStore


class RateRuleStore(GenericStore):
    """Store used to manage Source entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/rates_rules/
    """
    def __init__(self,credential_manager):
        super(RateRuleStore, self).__init__(credential_manager,"rates_rules")
