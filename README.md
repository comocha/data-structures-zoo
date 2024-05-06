# interview-template-python

Template for interviewing using my own environment

# Getting Started

## Prerequisites

Ensure the following are installed on your system:

- `python 3.12` (https://www.python.org/downloads/). 
- `pip` (https://pip.pypa.io/en/stable/installation/)
- `pipenv` (https://pipenv.pypa.io/en/latest/installation.html)
- `pyenv` (https://github.com/pyenv/pyenv)

## Installing

- use your terminal to navigate to the project root directory
- run `pipenv install` to install all project dependencies. 
  If you have `pyenv` installed, `pipenv` will prompt you to install the appropriate python version. The python version is specified in the `Pipfile` in the project workspace
- select correct interpreter in VSCode
  - open VSCode
  - press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac) to open the command palette
  - search for `select Python Interpreter` and select the command
  - search for the interpreter prefixes with the project root directory's name (should be `interview-templates-*`) and select it

## Usage

- `bash run.sh` to run the `main()` function
- `bash test.sh` to run all unit tests
- `pipenv` manages the Python environment
  - docs here: (https://pipenv.pypa.io/en/latest/)
  - `pipenv install {package-name}` to install a new package
  - `pipenv install --dev {package-name}` to install a dev package (libraries/tools for linting, unit testing, etc)
  - `pipenv run {command}` to run a command with the python environment active

## Editors
### VSCode
- There is a `settings.json` and `launch.json` to control the behavior of extensions and debugging.
- The extensions used are:
    - `mypy` for static type checking
    - [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) for formatting your code on save
    - The official [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension by Microsoft
    - [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) for LSP support.
    - [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint) for linting your code
    - [Python Debugger Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) for debugging through the editor.
#### Usage via VSCode
- Run Ctrl + F5 on `main.py` to run the main entry point, and on `test.py` to run the test suite
