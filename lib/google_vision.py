import io
import os
import urllib
import urllib.error
import logging
from typing import List, Optional

# Imports the Google Cloud client library
from google.cloud import vision

# Instantiates a client
client = vision.ImageAnnotatorClient()

def label_photo(file_name) -> Optional[List[str]]:
    # Loads the image into memory
    try:
        with urllib.request.urlopen(file_name) as image_file:
            content = image_file.read()

    except urllib.error.HTTPError as e:
        logging.warning(e)
        return

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    logging.debug('Successfully annotated photo')

    return [ label.description for label in labels ]
