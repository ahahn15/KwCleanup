
# - query Asset Service by keywords and image type (no illustrations, just stills/no video) and get assets
# - send images to Visint Service to get # of faces
# - show images with 0-1 faces
# - allow user to choose images to exclude from set
# - allow user to confirm removal of keywords on unselected images
# - make call to AKS to remove Family keywords


imgsToProcess = []

def getAssets():

# query Asset Service (returns Asset IDs)
# use delivery URL to get images

assetIds = assetService.get(asdfasdfasdf)
for each assetId in assetIds:
    url = get delivery url for assetIds
    populateImageArray(url)


def populateImageArray(url):
# for each image, call visint service (returns an integer >= 0)
# if number of faces is 0 - 1, then keep the image, otherwise remove it
numberOfFaces = visintservice.getFaces(url)
if (numberOfFaces < 2) add assetId to imgsToProcess

def removeKeywords():
# call AKS for each image ID to remove Family keywords (??)
# iterate through imgsToProcess array and make call to AKS