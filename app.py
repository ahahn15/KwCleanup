import requests
import uuid
import flask
import json

# - query Asset Service by keywords and image type (no illustrations, just stills/no video) and get assets
# - send images to Visint Service to get # of faces
# - show images with 0-1 faces
# - allow user to choose images to exclude from set
# - allow user to confirm removal of keywords on unselected images
# - make call to AKS to remove Family keywords

app = flask.Flask(__name__)

images = {"Images": []}


@app.route("/health")
def health():
    return "Ok"


@app.route("/assets", methods=["GET"])
def get_assets():
    coord_id = str(uuid.uuid4())
    token = get_token(coord_id)
    asset_service_url = 'http://usw2-stage-entsvc-asset.lower-getty.cloud'
    params = '?assettype=image&family=creative&phrase=family%20AND%20animal%20AND%20NOT%20(' \
             'Digitally%20generated%20image%20OR%20illustration)&pagesize=100&recency=last12months&deliverysizes=comp1024' \
             '&deliveryscheme=http&fields=deliveryurls'
    asset_url = asset_service_url + "/search" + params
    headers = {
        'Accept': 'application/json',
        'GI-Security-Token': token,
        'GI-Coordination-Id': coord_id
    }

    asset_service_response = requests.get(asset_url, headers=headers)
    assets = json.loads(str(asset_service_response.content, 'utf-8'))
    assets = assets['Assets']
    for asset in assets:
        asset_id = asset['Id']
        delivery_url = asset['DeliveryUrls']['Comp1024']
        assess_faces(asset_id, delivery_url)

    images_json = json.dumps(images)
    return images_json


def get_token(coord_id):
    token_url = 'https://usw2-stage-entsvc-securitytoken.lower-getty.cloud:443/SecurityToken/systems/1580/authenticate'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Gi-System-Password': 'systemPassword12345678==',
        'GI-Coordination-Id': coord_id
    }
    body = {'ActAsSystemId': 100}
    string_body = json.dumps(body)
    token_response = requests.post(token_url, json=json.loads(string_body), headers=headers)
    token = json.loads(str(token_response.content, 'utf-8'))['Token']
    return token


def assess_faces(asset_id, delivery_url):
    base_url = "http://visint-service.sandbox-getty.cloud/v1/faces/count?url="
    number_of_faces = requests.get(base_url + delivery_url)
    if number_of_faces.status_code != 200:
        print("invalid url: ", delivery_url)
    elif 0 <= int("".join(map(chr, number_of_faces.content))) < 2:
        images["Images"].append({"AssetId": asset_id, "Url": delivery_url})


def get_asset_keywords(asset_id):
    url = "http://10.196.34.15/AssetKeywordingService/AssetKeywordingService.asmx"
    headers = {'content-type': 'text/xml', 'SOAPAction': 'http://GettyImages.com/GetAssetKeywords', 'Content-Length': '534'}
    body_template = """<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><GetAssetKeywords xmlns="http://GettyImages.com/"><GetAssetKeywordsRequest xmlns="http://GettyImages.com/GetAssetKeywords.xsd"><MasterIDList><MasterID>1234</MasterID></MasterIDList><IncludeAncestors>true</IncludeAncestors><Mode>4</Mode></GetAssetKeywordsRequest></GetAssetKeywords></soap:Body></soap:Envelope>"""
    body = body_template.replace('1234', asset_id)
    response = requests.post(url, data=body, headers=headers)
    return response


def remove_asset_keywords():
    url = "http://akstest02.gettyimages.net/AssetKeywordingService/AssetKeywordingService.asmx"
    headers = {'content-type': 'text/xml', 'SOAPAction': 'http://GettyImages.com/SaveAssetDeltas'}
    body = """<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
              <soap:Body>
                <SaveAssetDeltas xmlns="http://GettyImages.com/">
                  <SaveAssetDeltasRequest xmlns="http://GettyImages.com/SaveAssetDeltasRequest.xsd">
                    <AssetDeltaSet>
                      <MasterIDs xmlns="http://GettyImages.com/AssetDelta.xsd">string</MasterIDs>
                      <MasterIDs xmlns="http://GettyImages.com/AssetDelta.xsd">string</MasterIDs>
                      <Deltas xmlns="http://GettyImages.com/AssetDelta.xsd">
                        <DeltaType>None or Insert or Delete or Upsert or Update or Clone or Replace</DeltaType>
                        <FieldType>Info or Metadata or Keyword or AmbiguousTerm or KeywordDaughters or None</FieldType>
                        <ItemID>int</ItemID>
                        <ItemValue>string</ItemValue>
                      </Deltas>
                      <Deltas xmlns="http://GettyImages.com/AssetDelta.xsd">
                        <DeltaType>None or Insert or Delete or Upsert or Update or Clone or Replace</DeltaType>
                        <FieldType>Info or Metadata or Keyword or AmbiguousTerm or KeywordDaughters or None</FieldType>
                        <ItemID>int</ItemID>
                        <ItemValue>string</ItemValue>
                      </Deltas>
                      <VitriaPublishPriority xmlns="http://GettyImages.com/AssetDelta.xsd">string</VitriaPublishPriority>
                      <BlockVitriaPublish xmlns="http://GettyImages.com/AssetDelta.xsd">boolean</BlockVitriaPublish>
                    </AssetDeltaSet>
                    <User>string</User>
                    <UserGroupCode>string</UserGroupCode>
                  </SaveAssetDeltasRequest>
                </SaveAssetDeltas>
              </soap:Body>
            </soap:Envelope>"""


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
