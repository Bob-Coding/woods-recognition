# Big data - woods

## Project Requirements

- `pipenv`: Pipenv is a tool that provides all necessary means to create a virtual environment for your Python project. It automatically manages project packages through the Pipfile file as you install or uninstall packages.

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

## Installing packages pipfile

To install all packages run:

```
$ pipenv install
```

Use environment:

```
$ pipenv shell
```
