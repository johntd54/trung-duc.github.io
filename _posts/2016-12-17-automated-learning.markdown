---
layout: post
title: "161217 - Automated learning"
date: 2016-12-17 21:25:13
categories: blog, ai
---

Feel embarrassed to know that Python interpreter (at least in Unix), does not require .py extension in script's filename to work. `python helloworld.py` is the same as `python helloworld` is the same as `python helloworld.csv`... As long as the script has correct Python syntax, it can be run by the Python interpreter regardless the extension of the script's filename.

Work on automated learning, built on top of Tensorflow.


Store configuration, either:

- Protobuf: serialized like Python's pickle
- JSON: human editable -> easier to manually create

For now, the application is not complicated and IO efficiency is not important, so JSON is better due to ease of use and human editable.

Must find a way to "efficiently" store numbers: weights and data. "Efficiently" in this case means small size. This is important since usually data size is large, and making clients download ~10GB of data may put them off, especially if they have slow Internet connection (like in Vietnam). If I can't find any way to limit the dataset below appropriate size, I should divide the dataset in small chunks and have the clients train the downloaded chunks simultaneously as they download the remaining chunks. Small file size is critically important for weights, as clients will have to upload trained weights to the server, and upload speed tends to be significantly slower than download speed, so smaller data size can speed up the uploading process, lower the chance of suffering from connection/uploading failure.

- `np.savetxt`
    + Saves np array to `.txt` file
    + Does not allow saving 3D array and above
    + So we need to flatten 3D array and above into 2D.
    + For large array, it takes forever to save
    + This method is not efficient. The SVHN training dataset is 175MB in `.mat` but 770MB in `.txt`.


- `np.save`
    + Saves np array to `.npy` file
    + Alllow multi-dimensional array
    + Pretty fast with average efficiency. 175MB `.mat` -> 215MB `.npy`
    + This method should work well for smaller array (maybe good for storing weights). The above 215MB `npy` data contain 225 million numbers. A large model has ~20 million numbers


- `np.savez`
    + Saves np arrays to a single, uncompressed `.npz` file
    + The file size is the same as `np.save`
    + Due to its ability to save multiple arrays into a single file, this method can work great to save weights (each weight is a distinctive array)


- `np.savez_compressed`
    + Saves multiple np arrays to a single compressed `.npz` file
    + Compared to `np.savez`, this method compresses 215MB of data to 171MB of data, which is even better than `.mat`. This is handy.
    + When load `.npz` saved by this method, use `np.load`. The loaded file is a dictionary-like structure, where each key corresponds to a numpy array.


To store data, can use:

- Amazon S3: paid
- **Dropbox**: preferred for unlimited data file and direct link. But not reliable since Dropbox will disable account of high traffic
- Box: does not support direct link
- ~**IDrive**: preferred for 5GB of free data, it seems like this service supports up to 2GB of maximum file size (web-based upload) or 10GB (app-based upload)~ Actually does not support direct link.
- **Google Drive**: preferred 15GB free data, direct link (https://drive.google.com/uc?export=download&id=FILE_ID), and Google brand name also guarantees a little bit security.

To inquire for which models to train, I should use Django Rest API. Client sends a GET request with optional parameters to the server. The server receives GET requests, processes the parameters, and returns a JSON response. These are the common requests and responses:

|...|Request|Response|
|--|-------|--------|
|1| List out information of all pending models | Return the information of all pending models and code to pick |
|2| Just run by default | Decide which model to train and send back training data and configuration |
|3| Request an explicit model to train | Send back training data and configuration for that model |

1-Request:
- /list
- authentication_param

2-Request:
- /default
- authentication_param

3- Request:
- /model
- authentication_param
- model_id

1-Response would be a list of dictionary, each dictionary contains:
- ID: id of model to train
- Dataset: name and description of dataset
- Model description: brief overview of the model

2/3-Response:
- ID: id of model to train
- Configuration: link to configuration file
- Dataset: [{url, file_name, dataset_name, size} ... list of links to dataset]


Download dataset:

- If any data files in the dataset exists, use those data files first to train, while at the same time download the remaining missing data files.
- Any data file downloaded should be added to training along with existing data file. Retrieval of missing data files must continues.


Train the model:

- Automatically construct the model based on configuration file.
- Periodically (say 2/hour or 1 every 1000 iterations or both or ...) save the weights to server. Hmm to save the weights use Django Rest API, or maybe use Google Drive API to upload weights to my folder
- Allow to resume training. Maybe I create a temp file that anytime the system starts, it checks whether there is any existing task
- Periodically (say 1 every 1000 iterations...) receive the message from server
- Should load the dataset in small blocks rather than loading the whole dataset, to avoid dataset that is larger than RAM



