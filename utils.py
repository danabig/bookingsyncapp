import copy
import csv
import json
import pdb

from bookingsynclord.constants import TEST_RENTAL_NAME, TEST_RENTAL_NAMES
from bookingsynclord.entities.NightlyRateMap import NightlyRateMap
from bookingsynclord.entities.Rental import Rental


def get_rental_by_name(rentals, name):
    for rental in rentals:
        if rental['name'] == name:
            return rental


def ensure_rental_entity_with_nightly_rates_managed_externally(booking_sync_api, rental, allow_manage):
    assert rental['name'] in TEST_RENTAL_NAMES

    _rental = copy.deepcopy(rental)
    rental_entity = Rental(_rental['id'])

    diff_json = {
        'id': _rental['id'],
        'nightly_rates_managed_externally': allow_manage
    }
    rental_entity.load_from_json(diff_json)
    booking_sync_api.rentals_store.put(rental_entity)


def updateNightlyRates(booking_sync_api, update_data):
    assert update_data['name'] in TEST_RENTAL_NAMES

    print "updating rates for %s" % update_data['name']
    nightly_rates_entity = NightlyRateMap()

    diff_json = {
                'id': update_data['id'],
                "minimum_stays_map": "3,3,3,3,3,3,3,3,3,3,3,3",
                "rates_map": "100,101,102,103,104,105,106,107,108,109,110",
                "start_date": "2018-07-07"
            }
    # nightly_rates_entity.load_from_json(diff_json)
    nightly_rates_entity.load_from_json(update_data)
    result = booking_sync_api.nightly_rates_map_store.put(nightly_rates_entity)
    print result
    print "update complete"

    # test_rental = next((x for x in rentals if x['name'] == TEST_RENTAL_NAME), None)
    # if test_rental:
    #     print "updating rates for %s" % TEST_RENTAL_NAME
    #     nightly_rates_entity = NightlyRateMap()
    #     diff_json = {
    #         'id': test_rental['links']['nightly_rate_map'],
    #         "minimum_stays_map": "3,3,3,3,3,3,3,3,3,3,3,3",
    #         "rates_map": "100,101,102,103,104,105,106,107,108,109,110",
    #         "start_date": "2018-07-07"
    #     }
    #     nightly_rates_entity.load_from_json(diff_json)
    #     booking_sync_api.nightly_rates_map_store.put(nightly_rates_entity)
    #     print "update complete"
    # else:
    #     print "%s doesnt exist" % TEST_RENTAL_NAME


def load_csv_data(rentals, file):
    rate_mappings = []
    csvreader = csv.reader(file)
    next(csvreader, None)
    for row in csvreader:
        rental_name = row[0]
        start_date = row[1]
        rate = row[2]
        min_stay = row[3]
        rate_map = [mapping for mapping in rate_mappings if 'name' in mapping and mapping['name'] == rental_name and mapping['start_date']]
        if len(rate_map) == 1:
            rate_map = rate_map[0]
        else:
            rate_map = create_mapping(name=rental_name, start_date=start_date)
            rate_mappings.append(rate_map)
        rate_map['minimum_stays_map'].append(min_stay)
        rate_map['rates_map'].append(rate)

    # adapt the object for bookingsync
    for map in rate_mappings:
        map['id'] = get_nightly_rate_map_id_by_name(rentals, map['name'])
        map['minimum_stays_map'] = ','.join(map['minimum_stays_map'])
        map['rates_map'] = ','.join(map['rates_map'])

    # print json.dumps(rate_mappings, indent=4, sort_keys=True)

    return rate_mappings


def create_mapping(name, start_date):
    return {
        'id': None,
        'name': name,
        'minimum_stays_map': [],
        'rates_map': [],
        'start_date': start_date
    }


def get_nightly_rate_map_id_by_name(rentals, name):
    name_rentals = [r for r in rentals if r['name'] == name]
    if len(name_rentals) == 1:
        return name_rentals[0]['links']['nightly_rate_map']
    else:
        assert False