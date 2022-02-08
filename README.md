# About this project
This is a human-in-the-loop experiment. That's it.

## Installation and execution
This guide is written for Linux/macOS. Running on Windows should be trivial. Make sure that you're running Python 3.6 or later.

### Installation

Navigate to the project root folder of the project. Create a virtual Python environment by running

```bash
python -m venv venv
```

if your Python 3 executable is called ```python3```, then run the above as

```bash
python3 -m venv venv
```

Activate the virtual environment by running (please note the leading period):

```bash
. venv/bin/activate
```

Install the dependencies buy running

```bash
cd backend
pip install -r requirements.txt
```

Finally, configure Flask by running

```bash
cd src
export FLASK_APP=app.py
```

That's it, you're done!

### Execution

Run the application by navigating to ```<project_root>/backend``` and activate the virtual environment by typing

```bash
. venv/bin/activate
```

Then, navigate to ```<project_root>/backend/src``` and execute by typing

```bash
python app.py
```

Starting up takes a little while, but once you're done, you can run the application in the browswer by navigating to [http://localhost:5000]() if you're using Flask. Close the application by hitting ```ctrl+c```.


## Execution environments

The experiment is designed to run on either a local PC or on AWS. It can even run the experiment itself on a local PC and save its results and sessions to AWS, rather than to the disk. While the execution environments themselves are equivalent, there are some differences when it comes to storage and web server options.

### Running on AWS

In order to run the experiment on AWS two things are needed: and EC2 instance and an S3 bucket. The experiment is rather hungry for computational power. Thus, a `c6g.4xlarge` instance is needed for decent performance. The experiment *should* be fairly easy to distribute across several EC2 instances, but this is currently untested.

### Storage

There are two storage backends made available to save the sessions and results of the experiments; a disk-based local storage and an AWS S3-based cloud storage. The disk-based storage uses [Pickle](https://docs.python.org/3/library/pickle.html) for all storage, while the cloud-based storage stores session data in Pickle, and experiment results in both JSON and Pickle formats.

### Web servers

The default web server used for development is [Flask's](https://flask.palletsprojects.com/en/2.0.x/) built in development server. It's fairly slow, but good for debugging purposes. For production development, a WSGI-based server should be used. This experiment uses [waitress](https://docs.pylonsproject.org/projects/waitress/en/latest/) as its default production server. It's a fair bit quicker than Flask and uses far fewer dependencies.

## Web interface

The experiment runs on a web server and uses a simple single-page application as a frontend, found in `frontend/index.html`. It connects to a REST-based web API published by the backend. The API uses HATEOAS to guide the frontend to its next step, and it is thus fairly easy to adapt to another frontend if deemed neccessary. The API base url is set in the configuration file, as specified below.

## Configuration

The experiment is fairly configurable, although some details still have to be done in code.

### The app.ini file

The bulk of settings are found in the `backend/src/config/app.ini` file. It has to be created, but a template is available as `backend/src/config/app.ini.example`. The config settings are described below:

|           Setting         |                                                Description                                                |
|---------------------------|-----------------------------------------------------------------------------------------------------------|
| **app**                   |                                                                                                           |
| mode                      | `development` for development, `production`for production                                                 |
| host                      | Decides which IP number to listen to. Use `0.0.0.0` for any address.                                      |
| port                      | Decides which port to listen to. Typically, `5000` is used for development and 80 or 8080 for deployment. |
| **backend**               |                                                                                                           |
| storage_backend           | `aws` for storage in AWS (see additional settings below), `disk` for local storage.                       |
| data_path                 | The location of the training data with a trailing slash, e.g., `data/`.                                   |
| data_features_name        | The name of the features file, e.g., `features.pickle`. This file is a pickled Python dictionary.         |
| im_indices_name           | The name of the inices file, e.g., `im_indicies.pickle`. This file is a pickled Python dictionary.        |
| sessions_path             | The location of the saved session data with a trailing slash, e.g., `session_data/`.                      |
| results_path              | The location of the saved results data with a trailing slash, e.g., `results/`.                           |
| default_nbr_of_images     | The default number of images in a image stream, e.g., 30. This can be changed in code as well.            |
| labels                    | A comma-separated list of labels that will accompany each image, e.g., `cat,dog`.                         |
| **api**                   |                                                                                                           |
| base_url                  | The base URL for the REST-based web API, e.g., `/api/v1`.                                                 |
| **frontend**              |                                                                                                           |
| frontend_base             | The location of the frontend files relative to the backend, e.g., `../../frontend`.                       |
| image_base                | The URL of the images used in the experiment, e.g., `http://cdn.somewhere.com/images/`.                   |
| image_directory           | The location of the UI images used for the frontend, e.g., `images/`.                                     |
| step_duration             | The number of seconds between each new image in a stream, e.g., `5`.                                      |
| subsession_pause_duration | The number of seconds between two sub sessions, e.g, `10`. Not used by the default fronend.               |
| **aws**                   |                                                                                                           |
| bucket                    | The name of a S3 bucket, in which results and sessions are to be stored.                                  |
| region                    | The region in where the experiment is being run, e.g., `eu-north-1`.                                      |
| access_key                | An IAM user's access key. The user needs to have full S3 privileges and be in the bucket's ACL.           |
| secret_access_key         | An IAM user's secret access key.                                                                          |

### The experiment set up in main_BE.py

The subsessions are defined in the `create_session()` method of main_be. The number of steps are set in the `nbr_of_steps` variable, which is used to create space for the different subsessions. Subsessions are then defined using the `create_subsession()` method, in which a strategy and end message are defined. In fact, the end message is mainly used as an introduction to the following subsession. When a subsession is created, it is added to a session step using `Session.add_subsession()`. The subsessions are then run in the order in which they're added to the subsession steps.

Two strategies are defined:
- Strategy.MT -- An ordinary machine teaching strategy. The user is in charge of wheter they give any feedback or not.
- Strategy.ALMT -- A strategy that uses active learning. The software will select some data points where user feedback is disabled.


## Training data
No training data is provided in this distribution. You can find the current training data at [https://www.kaggle.com/c/dogs-vs-cats/overview](). The location of the training data is specified in the config file (see above).