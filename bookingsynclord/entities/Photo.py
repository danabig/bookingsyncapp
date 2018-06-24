from Entity import Entity


class Photo(Entity):
    ENTITY_TYPE = "photos"
    """Represent a Photo element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/photos/
    """

    def __init__(self, id=None):
        return super(Photo, self).__init__("photos", id)
