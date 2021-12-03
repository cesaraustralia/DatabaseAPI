# API for Resistance database
 Flask API for PostgreSQL database

## Installing
First create a Python environment and activate it:

```bash
cd ~/DatabaseAPI
python -m venv ./venv

```

```bash
# cd ~/DatabaseAPI
source ./venv/bin/activate
```

Now install all the Python packages and save the into the `requirement.txt` file.

```bash
# install packages with pip
pip install flask flask_sqlalchemy

# freeze packages
pip freeze > requirement.txt
```

This will be used to install the required package in the docker image.
