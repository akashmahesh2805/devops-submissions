# Exercise 9 - Jenkins Multi-Stage Pipeline

A Jenkins Declarative Pipeline builds a virtual environment, installs the Flask dependency, runs the unit test, copies the app to `python-app-deploy`, and runs the same test against the deployed copy.

## Configure Jenkins

Create a Pipeline job using this repository's `Jenkinsfile` at `Exercise 9 - Jenkins Multi-Stage Pipeline/Jenkinsfile`. The Jenkins agent needs Python 3, `venv`, Git, and network access to install the listed dependency.

The pipeline stages are **Build**, **Test**, and **Deploy**. A successful run reports one passing test for the deployed Flask route.

## Run the test locally

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s . -p test_app.py
```
