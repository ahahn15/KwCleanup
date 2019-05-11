# KwCleanup
Part of a 2 day Hackathon project to use a facial recognition machine learning model to identify and remove misapplied keywords to Getty images.

## Background
Contributors often attach incorrect keywords to their images which affects the quality of search results on the main page. One particularly common misuse of keywords is to apply family-related terms like "brother", "mother", and "siblings" to images without people or images with only animals. In this project we use an existing internal facial recognition service to identify the number of faces in an image and determine whether there are incorrect keywords applied. If so, these images are highlighted in the UI and the user can either remove or add images to that set and then confirm that family keywords should be removed from the images.

The facial recognition API could be used for further keyword cleansing such as removing the keywords "one person" or "two people" from images where they do not apply. Automating such processes would significantly alleviate the recurring manual task of cleaning up keywords on newly ingested images.
