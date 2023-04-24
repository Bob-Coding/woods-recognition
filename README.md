# Big data - woods

## Project Requirements
* `pipenv`: Pipenv is a tool that provides all necessary means to create a virtual environment for your Python project. It automatically manages project packages through the Pipfile file as you install or uninstall packages.

## Install Pipenv
1. Run the following command to ensure you have pip installed in your system:
```
$ pip --version
```
You should expect to receive a system response indicating the pip version. If no pip is discovered, install it as described in the Installation Instructions. Alternatively, you can download and install Python from http://python.org.

2. Install pipenv by running the following command:
```
$ pip install --user pipenv
```
3. For your convenience, you might add the user base’s binary directory to your PATH environmental variable. If you skip this procedure, PyCharm will prompt you to specify the path to the pipenv executable when adding a pipenv environment.

### windows:
1. Run the following command:
    ```
    $ py -m site --user-site
    ```
    A sample output can be:

    C:\Users\jetbrains\AppData\Roaming\Python\Python37\site-packages


2. Replace site-packages with Scripts in this path to receive a string for adding to the PATH variable, for example:
    ```
    $ setx PATH "%PATH%;C:\Users\jetbrains\AppData\Roaming\Python\Python37\Scripts"
    ```
   
### linux
1. Run the following command to find the user base's binary directory:
    ```
    $ python -m site --user-base
    ```
    An example of output can be
    
    /Users/jetbrains/.local (macOS) or /home/jetbrains/.local (Linux)

2. Add bin to this path to receive a string for adding to the ~/.bashrc file, for example:
    ```
    $ export PATH="$PATH:/Users/jetbrains/.local/bin"
    ```
    Run the following command to make the changes effective:
    ```
    $ source ~/.bashrc
    ```
3. Ensure you have enabled bashrc in your bash_profile.

## Configure pipenv for an existing Python project﻿
1. Do one of the following:

   Click the Python Interpreter selector and choose Add New Interpreter.
   
   Press Ctrl+Alt+S to open Settings and go to Project: <project name> | Python Interpreter. Click the Add Interpreter link next to the list of the available interpreters.
   
   Click the Python Interpreter selector and choose Interpreter Settings. Click the Add Interpreter link next to the list of the available interpreters.

2. Select Add Local Interpreter.

3. In the left-hand pane of the Add Python Interpreter dialog, select Pipenv Environment.
   Adding a Pipenv environment
4. Choose the base interpreter from the list, or click Choose the base interpreter and find the desired Python executable in your file system.

5. If you have added the base binary directory to your PATH environmental variable, you don't need to set any additional options: the path to the pipenv executable will be autodetected.

   If the pipenv executable is not found, follow the pipenv installation procedure to discover the executable path, and then paste it in the Pipenv executable field.

6. Click **OK** to complete the task.


   Once all the steps are done, the new pipenv environment is set for your project and the packages listed in the Pipfile are installed.