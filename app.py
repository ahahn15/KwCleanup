import requests
import uuid
import flask

import requests
import json
imagesToProcess = []

# - query Asset Service by keywords and image type (no illustrations, just stills/no video) and get assets
# - send images to Visint Service to get # of faces
# - show images with 0-1 faces
# - allow user to choose images to exclude from set
# - allow user to confirm removal of keywords on unselected images
# - make call to AKS to remove Family keywords
app = flask.Flask(__name__)

images = {}


@app.route("/health")
def health():
    return "ok"


@app.route("/assets", methods=["GET"])
def get_assets():

    coord_id = str(uuid.uuid4())
    token = get_token(coord_id)

    asset_url = '$assetServiceUrl/assets?&fields=keywords&keywordfields=text&keywordtypes=specificpeople'
    headers = {
        'Accept': 'JsonMimeType',
        'GI-Security-Token': token,
        'GI-Coordination-Id': coord_id
    }
    asset_ids = requests.get(asset_url, headers=headers)
    for asset_id in asset_ids:
        assess_faces(asset_id)


def get_token(coord_id):

    token_url = 'https://usw2-stage-entsvc-securitytoken.lower-getty.cloud:443/SecurityToken/systems/1580/authenticate'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Gi-System-Password': 'systemPassword12345678==',
        'GI-Coordination-Id': coord_id
    }
    token = requests.post(token_url, json={1580}, headers=headers)
    return token


def assess_faces(asset_id):
    baseUrl = "http://visint-service.sandbox-getty.cloud/v1/faces/count?url="
    delivery_url = "http://media.stage-gettyimages.com/photos/happy-family-with-dog-sitting-together-in-cozy-living-room-picture-id909597982"
    number_of_faces_request = requests.get(baseUrl + delivery_url)
    number_of_faces = number_of_faces_request.json()

    if number_of_faces < 2:
    # add asset id to images to process array

    print(number_of_faces_request.status_code)
    print(number_of_faces_request.json())


def remove_keywords(asset_id):
    return 0

# def populateImageArray(imageUrl):
# # for each image, call visint service (returns an integer >= 0)
# # if number of faces is 0 - 1, then keep the image, otherwise remove it
# url = ""
# response = requests.post(url, imageUrl)
# numberOfFaces = visintservice.getFaces(url)
# if (numberOfFaces < 2) add assetId to imgsToProcess
#
# def removeKeywords():
# # call AKS for each image ID to remove Family keywords (??)
# # iterate through imgsToProcess array and make call to AKS


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
