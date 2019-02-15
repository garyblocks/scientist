# scientist
A practical toolbox for machine learning and statistical analysis

## Install
* currently only support mac os
* download the whole folder, and open terminal
* install pipenv and run `pipenv install` and `pipenv shell`
* then run `python app.py`

## Features
### load data
* now the app takes two types of data:
    * table data: csv file with header
    * text data: txt file

### views
#### Table View
* table view is used to look at the origin data
* large data frame is split with pagination
* to get a more general view, you can shuffle the data
* basic statics and correlation are also available
#### Plot View
* plot view will give a more abstract idea of the dataset through plots
* you can select which features you want to plot
* currently support: kde, histogram, line, box, bar and scatter matrix
#### Text View
* this is only for text data, we can read through the content

### preprocess
* we provide several scalers to scale the features
* popular encoders
* when the dataset is too large, drop columns, rows or just draw a sample
* different strategies to handle missing data

### clustering
* build clusters using the following algorithms
    * kmeans
    * hierarchical methods
    * affinity propagation
* visualize the clusters using popular plot methods
    * t-sne
    * radviz
    * top 2 pcas
    * hierarchical tree(only for hierarchical methods)
### classification
* support both biclass problems and multiclass problems
* lots of common classifiers
* train test split and cross validation
* basic metrics and confusion matrix
### regression
* linear regression with basic statistics
* glm (gamma)
### coincidence
