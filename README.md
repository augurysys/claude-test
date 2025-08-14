
# GenAI (Agents) Template

This service includes a RESTful API using FastAPI and an asynchronous NSQ consumer service, built with Python 3.10.

### [Folder Structure](STRUCTURE.md) 🔗

## Table of Contents

- [Setup](#setup)
- [Running the API](#running-the-api)
- [Running the NSQ Consumer](#running-the-nsq-consumer)
- [Run Configuration Example](#run-configuration-example)
- [Notes](#notes)
- [License](#license)

---

## Setup

### 1. Create a Python 3.10 Virtual Environment
# NOTE: if you dont have `pyenv` installed see [venv.md](venv.md) to set it up.


```bash
pyenv install 3.10.13
```

Make sure Python 3.10 is installed on your machine. You can check your version with:

```bash
python --version
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### 2. Install Dependencies
After cloning the repo, run these commands to install the dependencies (run it in the context of the repository)
```bash
pip install -r requirements.txt
```

```bash
pip install -r requirements-internal.txt
```

Common Problems:
1. problem :https://github.com unrecognized
   fix: add url settings to gitconfig
   ~ open ~/.gitconfig
   add the following lines:
      [url "git@github.com:"]
	      insteadOf = https://github.com/
   
   
---

## Environment variables
Before running, make sure you have your ODE .env file,
this service is like another service on the Cluster

---

## Running the API

```bash
If you use VSCode/Cursor just run it using 
Run -> Run
```

How this magic happens?
.vscode/launch.json file which you can edit if you want.


### PyCharm users
1. Open the project in PyCharm.
2. Create a Run Configuration with the following settings:
   - **Script Path**: `api/app.py`
   - **Python Interpreter**: Use the interpreter from your `.venv` folder or just create one using PyCharm
   - **Working Directory**: Project root
   - **Environment Variables**: use .env file


To start the API service manually:

```bash
python api/app.py
```

Make sure any necessary environment variables or configuration files required by `app.py` are set up beforehand.

---

## Running the NSQ Consumer

To run the NSQ consumer service:

```bash
python asyncronous/nsq/nsq_consumer.py
```

This script listens to NSQ topics and processes messages asynchronously. Ensure your NSQ daemon (`nsqd`) and lookupd are running and configured properly.

---

## Run Configuration Example

If you are using an IDE like PyCharm or VSCode, here’s how to configure run settings:

### API (`api/app.py`)

- **Script Path**: `api/app.py`
- **Python Interpreter**: Use the interpreter from your `venv`
- **Working Directory**: Project root
- **Environment Variables**: (if needed) e.g., `FLASK_ENV=development`

### NSQ Consumer (`asyncronous/nsq/nsq_consumer.py`)

- **Script Path**: `asyncronous/nsq/nsq_consumer.py`
- **Python Interpreter**: Use the interpreter from your `venv`
- **Working Directory**: Project root
- **Environment Variables**: (if needed) e.g., `NSQ_LOOKUPD_HOST=localhost`

---

## Notes

- Use `.env` files or other secret management strategies for sensitive configurations.
- Make sure NSQ services (`nsqd`, `nsqlookupd`, `mongodb`) are running and reachable from your consumer.

---

## License

MIT License (or update to your specific license)
