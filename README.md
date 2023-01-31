# Cloudera_Hackathon

## Summary:
This project uses machine learning methods to predict the selling price of an art piece at an auction, by taking in an image of the art and art attributes from the user. The application is split into two models, a numerical model that is trained on the selling prices of pieces based on their attribute values and a computer vision model uses a Convolutional Neural Network (CNN) that is trained on images of art pieces and their respective selling prices. The final price prediction is generated using a weighted average of the outputs of the two models. The user journey includes inputing an image of the art and various attributes associated with it including (Year of the painting, the time period, How famous the artist is, descriptions of the image, etc..), and the app will output the predicted selling price of that piece at an auction. 

## Data Aggregation

The data for the numerical model was taken from a premade dataset on Kaggle. The link to that data can be found here: https://www.kaggle.com/datasets/flkuhm/art-price-dataset. The data includes the following attributes: price, artist, Title, yearCreation, signed, condition, period, and movement.

The image data used to train the computer vision model is derived from the Sotheby's website, which has an online database of many art auction images of various movements and genres and the selling price for those movements. The website link can be found here: https://www.sothebys.com/en/buy/private-sales/contemporary-art?locale=en

After using web scraping techniques to generate a CSV file with the links to download all the images, we wrote a downloader script to download those images into a folder and split these folders by the movement of art. The downloader scripts can be found in the ImageDownloader folder (https://github.com/Idanlau/Cloudera_Hackathon/tree/main/scripts/ImageDownloader). 

## Numerical Model
After experimenting with 3 different models, Random forest regressor, Multiple linear regression and KNN regressor, Random Forest Regressor yeilded the best results and the metric used to evaluate the models were Mean Average Error. Preprocessing techniques to deal with categorical data was one hot encoding and for text based data, bag of words was used.


## Computer Vision
The computer vis

- bag of words
- random forest
- 
