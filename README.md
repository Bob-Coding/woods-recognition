# Big data - woods

## Project Requirements

- `pipenv`: Pipenv is a tool that provides all necessary means to create a virtual environment for your Python project. It automatically manages project packages through the Pipfile file as you install or uninstall packages.
- `environment variables`: For running the service there are few configurable options. First cd into ./service and add a .env file using the following vars:
  - `DATABASE_NAME`: Database name MongoDB (default: "woods_recognition")
  - `COLLECTION_NAME`: Collection name MongoDB (default: "dataset_cleaned")
  - `DATABASE_URL`: Mongo URI with db included (default: "mongodb://root:example@localhost:27017/woods_recognition?authSource=admin")
  - `TRAIN_SEQ_DENSE_MODEL`: Set "True" or "False" for training sequential dense model at start-up (default: "False")
  - `TRAIN_DENSE_MODEL`: Set "True" or "False" for training dense model at start-up (default: "False")
  - `API_URL`: API URL for swagger docs (default: http://localhost:5000)

## Install Pipenv

1. Run the following command to ensure you have pip installed in your system:

```
$ pip --version
```

You should expect to receive a system response indicating the pip version. If no pip is discovered, install it first. Alternatively, you can download and install Python from http://python.org.

2. Install pipenv by running the following command:

```
$ pip install --user pipenv
```

3. For your convenience, you might add the user base’s binary directory to your PATH environmental variable. If you skip this procedure, PyCharm will prompt you to specify the path to the pipenv executable when adding a pipenv environment.

## Running Service and UI

### Service

Navigate to the big-data-woods/service folder.
Create a virtualenv for this project:

```
$ pipenv install
```

Activate this project's virtualenv:

```
$ pipenv shell
```

Run service:

```
$ python app/main.py
```

### UI

Navigate to the big-data-woods/ui folder.
Install dependencies for this project:

```
$ npm install
```

Run UI in development mode:

```
$ npm run dev
```

Run UI in production mode:

```
$ npm run build
$ npm run start
```
