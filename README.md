# scientist
A practical toolbox for machine learning and statistical analysis

## Install
* currently only support mac os
* download the whole folder, and open terminal
* install pipenv and run `pipenv install` and `pipenv shell`
* then run `python app.py`

## Features
### start
* import a csv file(currenly only takes csv)

### view
#### Table View
* table view is to look at the origin data
* you can get a quick look of the dataset through viewing by page
* you can also shuffle the dataset to get a more general idea
* Basic statics and correlation are also available
#### Plot View
* plot view will give a more abstract idea of the dataset through plots
* you can select which features you want to plot
* currently support: kde, histogram, line, box, bar and scatter matrix

### preprocess
* you can scale the variables to 0-1 or normalize them by scaler
* or you can encode them by label, k hot or quatile by encoder
* when the dataset is too large, drop columns, rows or just draw a sample
* the software provides 4 strategies to deal with missing: drop the row, fill by mean/median or fill by the forward value

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
### regression
### coincidence
