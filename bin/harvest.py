import sys
import json
import logging
import argparse
from collections import defaultdict
from typing import Any, Dict, List
from pathlib import Path
from pymongo import MongoClient

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.tinder_api import authverif, get_recs_v2 as get_recommendations
from lib.io import read_json, write_json


def flatten(record: Dict[str, Any]):
    """
    Flattens a record of type=user returned by the Tinder API.

    >>> record = {
    ... "type": "user",
    ... "user": {
    ...     "_id": "aaaaaaaa",
    ...     "bio": "moved to Seattle for the rain",
    ...     "birth_date": "1992-03-16T20:52:25.409Z",
    ...     "name": "Devin"
    ... },
    ... "gender": 0,
    ... "distance_mi": 2
    ... }
    >>> flatten(record)
    {'type': 'user', 'gender': 0, 'distance_mi': 2, '_id': 'aaaaaaaa', 'bio': 'moved to Seattle for the rain', 'birth_date': '1992-03-16T20:52:25.409Z', 'name': 'Devin'}
    """
    user = record.pop('user')

    return {
        **record,
        **user
    }


def process_photos(user: Dict[str, Any], objects: Dict[str, int]) -> List[Dict[str, Any]]:
    """ """
    photos = user['photos']

    if not args.submit_images:
        logging.debug("User chose not to --submit-images")
        return

    logging.debug("Submitting image to Google Cloud Vision")
    from lib.google_vision import label_photo

    for photo in photos:

        labels = label_photo(photo['url'])

        if not labels:
            continue

        for label in labels:
            objects[label] += 1

    return objects


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description= __doc__,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--data-export",
        metavar="<data-export>",
        required=False,
        type=str,
        help="A filepath to a JSON of exported Tinder data.")

    parser.add_argument("--download-file",
        metavar="<download-from-tinder>",
        required=False,
        type=str,
        help="A filepath destination for the exported Tinder data.")

    parser.add_argument("--submit-images",
        metavar="<submit-images>",
        action="store_const",
        required=False,
        const=True,
        help="A boolean indicating whether or not to submit images to the cloud "
            "computer vision service.")

    args = parser.parse_args()

    if args.download_file:
        assert not args.data_export, "You should select either the --download-from-tinder or --data-export [file_path] options, but not both."
        logging.info(authverif())
        recs = get_recommendations()
        write_json(recs, 'data/recommendations.json')

    else:
        assert args.data_export, "You must specify either a --download-file or a --data-export"
        recs = read_json(args.data_export)

    assert recs['meta']['status'] == 200, "Something went wrong"
    recs = recs['data']['results']

    results = {}

    with MongoClient('mongodb://localhost:9999') as client:
        db = client.tinder
        users = db.users
        for record in recs:
            record = flatten(record)
            # Update the database
            users.update_one(
                { '_id': record['_id'] },
                { '$set': record },
                upsert=True)

    if args.submit_images:
        objects = defaultdict(int)
        write_json(process_photos(record, objects), 'data/objects.json')
