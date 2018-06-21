import requests
import uuid

# - query Asset Service by keywords and image type (no illustrations, just stills/no video) and get assets
# - send images to Visint Service to get # of faces
# - show images with 0-1 faces
# - allow user to choose images to exclude from set
# - allow user to confirm removal of keywords on unselected images
# - make call to AKS to remove Family keywords

images = {}


def get_assets():

    # get token
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