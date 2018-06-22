import requests
import uuid
import flask
import json
import threading
from queue import Queue
import time

# 1. query Asset Service by keywords (Family and Animals) and image type (no illustrations, just stills/no video)
# 2. send images to Visint Service to get # of faces
# 3. only return images with 0-1 faces (we don't want family keywords on images with no ppl or individuals)
# 4. user chooses images to exclude from set and confirms removal of keywords
# 5. make call to AKS to remove Family keywords from assets

app = flask.Flask(__name__)

images = {"Images": []}
url_queue = Queue()
print_lock = threading.Lock()
family_terms = ['family', 'dad', 'daughter', 'father', 'children', 'boys', 'girls', 'son']


@app.route("/health")
def health():
    return "Ok"


@app.route("/assets", methods=["GET"])
def get_assets():
    global images
    images = {"Images": []}
    coord_id = str(uuid.uuid4())
    token = __get_token(coord_id)
    assets = __call_asset_service(token, coord_id)
    print("Retrieved ", len(assets), " assets")

    for asset in assets:
        asset_id = asset['Id']
        delivery_url = asset['DeliveryUrls']['Comp1024']
        if any(term in delivery_url for term in family_terms):
            continue
        else:
            url_queue.put((asset_id, delivery_url))

    print("Elements in queue: ", url_queue.qsize())
    start = time.time()
    for i in range(50):
        t = threading.Thread(target=__process_queue)
        t.daemon = True
        t.start()

    url_queue.join()
    print("Execution time = {0:.5f}".format(time.time() - start))
    images_json = json.dumps(images)
    return images_json


@app.route("/remove")
def remove_asset_keywords(asset_id_array):
    url = "http://seafrewebaskstg.sea.amer.gettywan.com/AssetKeywordingService/AssetKeywordingService.asmx"
    headers = {'content-type': 'text/xml', 'SOAPAction': 'http://GettyImages.com/SaveAssetDeltas', 'Content-Length': '9385'}
    body_template = """<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><SaveAssetDeltas xmlns="http://GettyImages.com/"><SaveAssetDeltasRequest xmlns="http://GettyImages.com/SaveAssetDeltasRequest.xsd"><AssetDeltaSet><MasterIDs xmlns="http://GettyImages.com/AssetDelta.xsd">1234</MasterIDs><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61837</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61845</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61851</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>161039</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>235275</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>97626</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61868</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>116105</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>7376215</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61804</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61813</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>235276</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>158962</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61841</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61842</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>83167</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61847</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61849</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61855</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61859</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>101590</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>101455</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>138437</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61809</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61807</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>150719</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61833</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61831</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61934</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>102349</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61925</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>101885</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>101884</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61873</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>251770</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>251772</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61895</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>251771</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>13760281</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>13760280</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>83558</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61843</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>76406</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>127160</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>249954</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>249955</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>249956</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>106588</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>80636</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>150555</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>80635</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>7984452</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>7984451</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>1324684</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>807748</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>102033</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>3952590</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>9102255</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>78079</ItemID></Deltas><Deltas xmlns="http://GettyImages.com/AssetDelta.xsd"><DeltaType>Delete</DeltaType><FieldType>Keyword</FieldType><ItemID>61862</ItemID></Deltas><VitriaPublishPriority xmlns="http://GettyImages.com/AssetDelta.xsd">string</VitriaPublishPriority><BlockVitriaPublish xmlns="http://GettyImages.com/AssetDelta.xsd">false</BlockVitriaPublish></AssetDeltaSet><User>string</User><UserGroupCode>string</UserGroupCode></SaveAssetDeltasRequest></SaveAssetDeltas></soap:Body></soap:Envelope>"""

    for asset in asset_id_array:
        body = body_template.replace('1234', asset)
        response = requests.post(url, data=body, headers=headers)
        print(response.content)


def __get_token(coord_id):
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


def __call_asset_service(token, coord_id):
    asset_service_url = 'http://usw2-stage-entsvc-asset.lower-getty.cloud'
    params = '?assettype=image&family=creative&phrase=family%20AND%20animal%20AND%20NOT%20(' \
             'Digitally%20generated%20image%20OR%20illustration)&pagesize=100&begindate=1%2F1%2F2013&enddate=1%2F1%2F2015&deliverysizes' \
             '=comp1024&deliveryscheme=http&fields=deliveryurls'
    asset_url = asset_service_url + "/search" + params
    headers = {
        'Accept': 'application/json',
        'GI-Security-Token': token,
        'GI-Coordination-Id': coord_id
    }

    asset_service_response = requests.get(asset_url, headers=headers)
    assets = json.loads(str(asset_service_response.content, 'utf-8'))
    return assets['Assets']


def __process_queue():
    while True:
        asset_id, delivery_url = url_queue.get()
        __assess_faces(asset_id, delivery_url)
        url_queue.task_done()


def __assess_faces(asset_id, delivery_url):
    base_url = "http://visint-service.sandbox-getty.cloud/v1/faces/count?url="
    number_of_faces = requests.get(base_url + delivery_url)
    if number_of_faces.status_code != 200:
        with print_lock:
            print("Invalid url: ", delivery_url)
    elif int("".join(map(chr, number_of_faces.content))) > 1:
        with print_lock:
            print("Removing image from array: ", delivery_url)
    else:
        images["Images"].append({"AssetId": asset_id, "Url": delivery_url})


def __get_asset_keywords(asset_id):
    url = "http://seafrewebaskstg.sea.amer.gettywan.com/AssetKeywordingService/AssetKeywordingService.asmx"
    headers = {'content-type': 'text/xml', 'SOAPAction': 'http://GettyImages.com/GetAssetKeywords', 'Content-Length': '534'}
    body_template = """<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><GetAssetKeywords xmlns="http://GettyImages.com/"><GetAssetKeywordsRequest xmlns="http://GettyImages.com/GetAssetKeywords.xsd"><MasterIDList><MasterID>1234</MasterID></MasterIDList><IncludeAncestors>true</IncludeAncestors><Mode>4</Mode></GetAssetKeywordsRequest></GetAssetKeywords></soap:Body></soap:Envelope>"""
    body = body_template.replace('1234', asset_id)
    response = requests.post(url, data=body, headers=headers)
    print(response.content)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
