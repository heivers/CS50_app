# CS50 - Pet Classifier
#### Video Demo:  https://youtu.be/r31x--mcxNM
#### App: https://cs50-bart.herokuapp.com/
#### Description:

## The idea

The idea of this project was more or less born while going through some TensorFlow / Fastai literature, courses.\
One of the projects was to create a Dog or Cat classifier. It worked quite well, so I decided to take it one step further
and try to classify several breeds of dogs and cats.
I used the dataset that was described in the FastAI book as it has about 200 pictures per breed and that seems to be a good
number for doing transfer learning.

## 1. The Model

Dataset: Oxford-IIIT Pet Dataset - Tensorflow Datasets (split into training, validation, test)\
The training dataset contained about 6400 images, the other 1000 were divided in validation and test.\
Data Preparation: Resize and Rescale to make it easier and faster for the model to learn\
Augmentation on Training Data to "increase" the number of training images.\
Pre-Trained Model: Initally tried InceptionV3, but the resulting model was about 500GB. Even in Tensorflow Lite too big too publish \
Reverted to using MobilenetV2, as this model is deliberately kept smaller, so it can run on mobile phones etc...\
Initial Training: only prediction layers were added, so the number of trainable layers was 2 - .\
Validation accuracy before training was around 2% and went up quickly. After about 10 epochs, validation accuracy already at 80%\
Fine Tuning: Too make the model predict even better, fine tuned by making the last ~50 layers trainable. - Continued training for several more epochs. Validation accuracy improved to around 90%\
Test the model: Run the model on never seen before test data before deployment: Accuracy about 88%.
\
## 2. Convert Model for Inferencing

Model saved and converted to a TensorFlow Lite Model.\
Size of the TF Lite Model approx. 8MB.

## 3. The App

Build a Flask app around the model. Created a home page with the supported breeds.\
A classify page to upload an image and classify. When everything is ok, it's routed to the result page.\
Initially I showed all results, changed this to cannot classify if model is less than 70% sure.\
Also added an about this project page, with a little info on me and a short explanation for the App.\
App deployed at https://cs50-bart.herokuapp.com/

## 4. Using the App.

You can go to https://cs50-bart.herokuapp.com/. On the home page, you will see a table with supported breeds.\
To make a prediction either click on the "click here" or go to the Pet Classifier in the menu.\
In the pet classifier, you can upload a jpeg/jpg Image. All other extensions are rejected. Not choosing a file is also treated with a flash error message.\
After selecting a picture, you click on classify. This invokes the Tensorflow Lite Interpreter. \
The App will open the results page.\
If the interpreter is more than 70% certain, the dog or cat belongs to one of the known breeds, it will show the breed and the probability the model assigns to it.\
With less than 70%, the message will say that it cannot be classified.\
\
You can also look at the About This Project page to learn a bit more about the project.

## 5. Future enhancements
More breeds: Using different datasets, trying to incorporate more breeds into the app.\
There's a Stanford Dogs dataset and I found scraped data online with many cat examples.\
Upload feature: If the dog or cat is wrongly classified or cannot be classified. Present an upload feature, to upload the picture of the animal and a label.