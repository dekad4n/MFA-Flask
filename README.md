# Installation <br/>

Firs check your pip version with:
```
pip --version <br/>
```
If not installed go to to website and install with python:
for Windows: https://www.geeksforgeeks.org/how-to-install-pip-on-windows/
for Mac: Just use brew with command 
```
brew install python
```
Homebrew will install the latest version of Python (including PIP)

<br/>
How to install brew?  https://docs.brew.sh/Installation
<br/>

### Install pipenv<br/>
Check this website for your OS to follow instructions if you had any problem
https://pipenv.pypa.io/en/latest/install/ <br/>

Install pipenv on Mac with brew:
```
brew install pipenv
```
Install pipenv on Windows:
```
pip install pipenv
```
### Create your environment:
Note: after installing pipenv everything will be easier just open a terminal or command promt on the folder called "loginApp" where the "Pipfile" stored.

After cd to loginApp
MacOS or Windows:
```
pipenv install
```
You can activate your environment but you don't have to
### Activate the environment in MacOS:
```
. <name of env>/bin/activate
```
### Activate the environment in Windows:
```
<name of env>\Scripts\activate
```

Now your environment is ready now its time to setup db:
1- install docker desktop if you didn't from official website
2- cd into cs437 folder on your terminal or command prompt
3- test if docker is working with ```docker --version``` command
4- if you can see your version evderything is okay
5- just run te ```docker compose up``` command in the cs437 folder.
6- wait for 1-2 min anc you can shut down your terminal or press ctrl-C
7- now you will see your mongo container in Docker Desktop
8- install MongoDB Compass 
9- use ```mongodb://admin:pass@localhost:27017/``` string to connect to mongodb
10- if this doesn't work try ```mongodb://localhost:27017/```
11- after connecting to your mongo instance create db from lest section and give the name "loginApp" and write "User" to collection name

note: on the initial run of app an instance called userEx will be added to db id doesn't exist

        user = {
            "username": "exUser",
            "password": generate_password_hash("123456789"),
            "email": "exUser@gmail.com",
            "recoveryPhrase": generate_password_hash("annemin kizlik soyadi")
        }

How to setup your flask app:
- One method is to cd to you "loginApp" folder, activate your venv, and run "python app.py" or "python3 app.py" command

- Another method which I prefer is create a launch.json file if you're using VScode
- My example launch.json file in the .vscode folder but it is set for MacOS
- But by changing the ```"python": "${workspaceFolder}/loginApp/.venv/bin/python3.10"``` to your venv path it should work as well
- launch.json example
<img width="487" alt="Screen Shot 2022-12-19 at 16 56 27" src="https://user-images.githubusercontent.com/94080241/208441754-6aa75e98-1a1c-48db-97e7-7b664f688755.png">

If I miss anything just reach me
