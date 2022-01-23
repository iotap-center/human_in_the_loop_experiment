# HITR
This is the HITR experiment

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
flask run
```

Starting up takes a little while, but once you're done, you can run the application in the browswer by navigating to [http://localhost:5000](). Close the application by hitting ```ctrl+c```.


## Training data
The training data is placed in backend/src/data/.

No training data is provided in this distribution. You can find the current training data at ADD LINK HERE.