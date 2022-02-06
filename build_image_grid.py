from email.mime import base
import glob
import os
import logging
import re

import matplotlib
import matplotlib.pyplot as plot
import matplotlib.image as mpimg

matplotlib.use('TkAgg')

from os.path import normpath, basename

logging.basicConfig(level=logging.DEBUG)

image_name_extractor = re.compile(r"^(?P<country>\w+)_(?P<lat>[\d\.\-]+)_(?P<long>[\d\.\-]+)\.\w+$")

def build_image_grid(image_directory):
    image_wildcard_path = os.path.join(image_directory, "*")
    image_filepaths = glob.glob(image_wildcard_path)

    images = list()

    for filepath in image_filepaths:
        image_basename = basename(normpath(filepath))
        match = image_name_extractor.match(image_basename)

        if match is None:
            logging.warn(f"Failed to match on name {filepath}.")
            continue

        images.append({
            "country": match.group("country"),
            "latitude": float(match.group("lat")),
            "longitude": float(match.group("long")),
            "image": mpimg.imread(filepath)
        })

    longitudes = sorted(list({image.get("longitude") for image in images}))
    latitudes = sorted(list({image.get("latitude") for image in images}))

    fig, axes = plot.subplots(len(latitudes), len(longitudes))

    for image in images:

        row = latitudes.index(image["latitude"])
        col = longitudes.index(image["longitude"])

        axes[row, col].imshow(image["image"])
        axes[row, col].axis("off")
    
    plot.show()

if __name__ == "__main__":

    build_image_grid("./images/")