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

Now install all the Python packages and save the into the `requirements.txt` file.

```bash
# install packages with pip
pip install flask flask_sqlalchemy

# freeze packages
pip freeze > requirements.txt
```

This will be used to install the required package in the docker image.

Use `pip` to install the packages in a different system or in docker images:

```bash
pip install -r requirements.txt
```