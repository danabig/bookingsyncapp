from abc import ABCMeta
import bookingsynclord.config
import requests
import logging
from bookingsynclord.entities import entity_generator

logger = logging.getLogger(__name__)


class GenericStore:
    """Abstract class with common properties for all Store."""
    __metaclass__ = ABCMeta

    def __init__(self, credential_manager, entity_type):
        self.credential_manager = credential_manager
        self.entity_type = entity_type

    @staticmethod
    def build_url(endpoint):
        """used to build url parameter of request done to API
        :param endpoint: endpoint details defined by BookingSync(for example /bookings to list booking)
        :type  endpoin : string or unicode

        :rtype: <string:absolute URL of the endpoint
        """
        return bookingsynclord.config.APIURL_ENDPOINT + endpoint

    def get_endpoint(self, action, entity=None):
        """Get the value of the endpoint for an action.

        For example, to get the endpoint to list all bookings (/bookings)
        you would use this function with action=LIST.

        All API endpoints usable are defined in the config.
        :param action: Action you intend to do (CREATE,LIST,GET)
        :type  action: String
        :param entity: required for Action relative to a specific entity instance
        :type  entity: entities.Entity

        :rtype: <string:endpoint value>
        """
        if entity is None:
            return bookingsynclord.config.BOOKINGSYNC_ENDPOINT[self.entity_type][action]
        else:
            print entity.key_mapping()
            template = bookingsynclord.config.BOOKINGSYNC_ENDPOINT[self.entity_type][action]
            return(template.format(**entity.key_mapping()))

    def get_request_bookingsync(self, url, page=1, filters={}):
        """Send request to bookingSync and return Json format object.
        Pass the credential in the header.

        :param url: url to post request to.
        """
        headers = {'Authorization': 'Bearer {}'.format(self.credential_manager.access_token)}
        params = {}
        if page > 1:
            params['page'] = page
        for key, value in filters.items():
            params[key] = value
        json_r = requests.get(url=url, headers=headers, params=params)
        json_r.raise_for_status()
        json = json_r.json()
        if json_r.headers.get('X-Total-Pages', 0) > 1:
            json['max-page'] = json_r.headers.get('X-Total-Pages', 0)
            json['current-page'] = page
        return json

    def post_request_bookingsync(self, url, data):
        """Send POST request to bookingSync and return Json format object.
        Pass the credential in the header.

        :param url: url to post request to.
        """
        headers = {'Authorization': 'Bearer {}'.format(self.credential_manager.access_token)}
        print data
        json_r = requests.post(url=url, headers=headers, json=data)
        json_r.raise_for_status()
        return json_r.json()

    def put_request_bookingsync(self, url, data):
        """Send POST request to bookingSync and return Json format object.
        Pass the credential in the header.

        :param url: url to post request to.
        """
        headers = {'Authorization': 'Bearer {}'.format(self.credential_manager.access_token)}
        print data
        json_r = requests.put(url=url, headers=headers, json=data)
        json_r.raise_for_status()
        return json_r.json()

    def delete_request_bookingsync(self, url):
        """Send DELETE request to bookingSync.
        Pass the credential in the header.

        :param url: url to post request to.
        """
        headers = {'Authorization': 'Bearer {}'.format(self.credential_manager.access_token)}
        r = requests.delete(url=url, headers=headers)
        r.raise_for_status()
        return r.status_code

    def post(self, entity):
        """API POST call to create entity.
        :param entity: Entity to create.
        :type  entity: bookingsynclord.entities.Entity
        :rtype        : bookingsynclord.entities.Entity, entity created
        """

        logger.debug("Calling POST for entity : {}".format(self.entity_type))
        endpoint = self.get_endpoint("POST", entity)
        url = GenericStore.build_url(endpoint)
        json = self.post_request_bookingsync(url, entity._to_json_list())
        entity.id = json[entity.entity_type][0]['id']
        return entity

    def delete(self, entity):
        """API delete call on entity.
        :param entity: Entity to delete.
        :type  entity: bookingsynclord.entities.Entity
        :rype        : int, status code of request
        """
        logger.debug("Calling DELETE for entity : {}".format(self.entity_type))
        endpoint = self.get_endpoint("DELETE", entity)
        url = GenericStore.build_url(endpoint)
        r = self.delete_request_bookingsync(url)
        return r

    def put(self, entity):
        """API PUT call to update entity.
        :param entity: Entity to update.
        :type  entity: bookingsynclord.entities.Entity
        :rype        : int, status code of request
        """

        logger.debug("Calling PUT for entity : {}".format(self.entity_type))
        endpoint = self.get_endpoint("PUT", entity)
        url = GenericStore.build_url(endpoint)
        r = self.put_request_bookingsync(url, entity._to_json_list())
        return r

    def list_json(self, page=1, filters={}):
        """return json containing the result of list call.
        :rtype: dict / Json loaded object
        """
        logger.debug("Calling list_json for entity : {}".format(self.entity_type))
        endpoint = self.get_endpoint("LIST")
        url = GenericStore.build_url(endpoint)
        logger.debug("URL generated : {}".format(url))

        json = self.get_request_bookingsync(url, page=page, filters=filters)
        return json

    def get(self, id, filters={}):
        """return a single element of entity
        :param id: ID of the element queried
        :type  id: string or integer
        :rtype: entities.Entity
        """
        json = self.get_json_by_id(int(id), filters=filters)
        new_entity = entity_generator(self.entity_type)()
        new_entity.load_from_json(json[self.entity_type][0])
        return new_entity

    def get_json_by_id(self, id, filters={}):
        """return a single element of entity in JSON format
        :param id: ID of the element queried
        :type  id: string or integer
        :rtype: dict / Json loaded object
        """
        logger.debug("Calling get_json_by_id for entity : {}".format(self.entity_type))
        endpoint = self.get_endpoint("GET")
        url = GenericStore.build_url(endpoint.format(id=str(id)))
        logger.debug("URL generated : {}".format(url))
        json = self.get_request_bookingsync(url, filters=filters)
        logger.debug("returned : {}".format(json))
        return json
