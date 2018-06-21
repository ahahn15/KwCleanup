

import requests
import json
imagesToProcess = []


def populateImageArray():

    baseUrl = "http://visint-service.sandbox-getty.cloud/v1/faces/count?url="
    delivery_url = "http://media.stage-gettyimages.com/photos/happy-family-with-dog-sitting-together-in-cozy-living-room-picture-id909597982"
    number_of_faces_request = requests.get(baseUrl + delivery_url)
    number_of_faces = number_of_faces_request.json()

    if number_of_faces < 2:
        #add asset id to images to process array

    print(number_of_faces_request.status_code)
    print(number_of_faces_request.json())