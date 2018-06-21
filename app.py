import requests
import uuid
import flask

import requests
import json

import xml.etree.ElementTree as ET


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


def assess_faces(asset_id, delivery_url):
    # asset_id = "847742514"
    # delivery_url = "http://media.stage-gettyimages.com/photos/dog-standing-on-ice-wearing-christmas-booties-picture-id847742514?s=612x612"
    base_url = "http://visint-service.sandbox-getty.cloud/v1/faces/count?url="
    number_of_faces_request = requests.get(base_url + delivery_url)
    number_of_faces = number_of_faces_request.json()

    print(number_of_faces_request.status_code)

    if 0 <= number_of_faces < 2:
        images[asset_id] = delivery_url

    print(json.dumps(images))






def get_asset_keywords():
    url = "http://seafrewebaskstg.sea.amer.gettywan.com/AssetKeywordingService/AssetKeywordingService.asmx"
    headers = {'content-type': 'text/xml', 'SOAPAction': 'http://GettyImages.com/GetAssetKeywords', 'Content-Length': '1512'}
    body = """<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><GetAssetKeywords xmlns="http://GettyImages.com/"><GetAssetKeywordsRequest xmlns="http://GettyImages.com/GetAssetKeywords.xsd"><MasterIDList><MasterID>90000291</MasterID></MasterIDList><IncludeAncestors>true</IncludeAncestors><Mode>4</Mode></GetAssetKeywordsRequest></GetAssetKeywords></soap:Body></soap:Envelope>"""

    response = requests.post(url, data=body, headers=headers)
    print(response.content)
    print(response.status_code)
    # fist try and git the assetkeywordservice to see if if can return the right things
    # loop through asset_id_array and remove all family keywords associated (SaveAssetDeltas)

def remove_asset_keywords():
    url = "http://seafrewebaskstg.sea.amer.gettywan.com/AssetKeywordingService/AssetKeywordingService.asmx"
    headers = {'content-type': 'text/xml', 'SOAPAction': 'http://GettyImages.com/SaveAssetDeltas'}
    body = """<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><SaveAssetDeltas xmlns="http://GettyImages.com/"><SaveAssetDeltasRequest xmlns="http://GettyImages.com/SaveAssetDeltasRequest.xsd"><AssetDeltaSet><MasterIDs xmlns="http://GettyImages.com/AssetDelta.xsd">string</MasterIDs><MasterIDs xmlns="http://GettyImages.com/AssetDelta.xsd">string</MasterIDs><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>None or Insert or Delete or Upsert or Update or Clone or Replace</DeltaType><FieldType>Info or Metadata or Keyword or AmbiguousTerm or KeywordDaughters or None</FieldType><ItemID>int</ItemID><ItemValue>string</ItemValue></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>None or Insert or Delete or Upsert or Update or Clone or Replace</DeltaType><FieldType>Info or Metadata or Keyword or AmbiguousTerm or KeywordDaughters or None</FieldType><ItemID>int</ItemID><ItemValue>string</ItemValue></Deltas><VitriaPublishPriority xmlns="http://GettyImages.com/AssetDelta.xsd">string</VitriaPublishPriority><BlockVitriaPublish xmlns="http://GettyImages.com/AssetDelta.xsd">boolean</BlockVitriaPublish></AssetDeltaSet><User>string</User><UserGroupCode>string</UserGroupCode></SaveAssetDeltasRequest></SaveAssetDeltas></soap:Body></soap:Envelope>"""

# # call AKS for each image ID to remove Family keywords (??)
# # iterate through imgsToProcess array and make call to AKS


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
