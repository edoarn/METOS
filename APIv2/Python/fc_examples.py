import os
import fc_api
import pprint
import json
from datetime import datetime
from dotenv import load_dotenv
from urllib import request
from urllib.error import HTTPError
from tqdm import tqdm


if __name__ == "__main__":
    load_dotenv()
    uri = 'https://api.fieldclimate.com/v2'

    #take this keys from https://ng.fieldclimate.com > User menu > API services > GENERATE NEW
    publicKey = os.getenv("METOS_PUBLIC_KEY")
    privateKey = os.getenv("METOS_PRIVATE_KEY")
    station_id = os.getenv("METOS_STATION_ID")     # an example demo station
    destination = os.getenv("METOS_DATA_DIR")

    api = fc_api.FcApi(uri, publicKey, privateKey)

    dates = api.get(f'/camera/{station_id}/photos/info').json()
    pprint.pprint(dates)

    first = int(datetime.strptime(dates["first"], "%Y-%m-%d %H:%M:%S").timestamp())
    last  = int(datetime.strptime(dates["last"], "%Y-%m-%d %H:%M:%S").timestamp())
    photos = api.get(f"/camera/{station_id}/photos/from/{first}/to/{last}/0").json()
    # store metadata (image info, bboxes, urls...)
    with open(os.path.join(destination, "data.json"), "w", encoding="utf-8") as f:
        json.dump(photos, f, indent=4)
    # store each image
    for data in tqdm(photos):
        url = None
        try:
            url = data["url"]
            name = url.split("/")[-1]
            request.urlretrieve(url, os.path.join(destination, "images", name))
        except HTTPError:
            print(f"{url} not found")
