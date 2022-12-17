# Installation <br/>
### Install virtualenv on MacOS <br/>
After installing python, install virtualenv on MacOS: <br />
```
sudo python -m pip install virtualenv
```
Install virtualenv on Windows (The code for MacOS works as well for new versions):
```
py -m pip install virtualenv
```
### Create an environment in MacOS:
```
python3 -m venv <name of environment>
```
### Create an environment in Windows:
```
py -m venv <name of environment>
```
### Activate the environment in MacOS:
```
. <name of env>/bin/activate
```
### Activate the environment in Windows:
```
<name of env>\Scripts\activate
```
### Install Flask 
```
pip install Flask
```
### Go to codes file
```
cd codes
```
### Set environment variablese in MacOS
```
export FLASK_APP=app.py
```
### Set environment variablese in Windows:
```
setx FLASK_APP "app.py"
```
### Run the project (always run the project when you are in codes file):
```
flask run
```

