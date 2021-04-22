# CS50 - Pet Classifier
#### Video Demo:  https://youtu.be/r31x--mcxNM
#### App: https://cs50-bart.herokuapp.com/
#### Description:
## 1. The Model

Dataset: Oxford-IIIT Pet Dataset - Tensorflow Datasets (split into training, validation, test)\
Data Preparation: Resize and Rescale. Augmentation on Training Data\
Pre-Trained Model: MobilenetV2\
Initial Training: only prediction layers added - Val. accuracy approx. 80%\
Fine Tuning: last ~50 layers trained - Val. accuracy approx. 87%\
\
## 2. Convert Model for Inferencing

Model saved and converted to a TensorFlow Lite Model.\
Size of the TF Lite Model approx. 8MB.

## 3. The App

Flask App to classify several breeds of Cats and Dogs.\
App deployed at https://cs50-bart.herokuapp.com/