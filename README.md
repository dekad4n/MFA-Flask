# Installation <br/>

Firs check your pip version with:<br/>
```
pip --version <br/>
```
If not installed go to to website and install with python:<br/>
for Windows: https://www.geeksforgeeks.org/how-to-install-pip-on-windows/<br/>
for Mac: Just use brew with command <br/>
```
brew install python
```
Homebrew will install the latest version of Python (including PIP)

<br/>
How to install brew?  https://docs.brew.sh/Installation
<br/>

### Install pipenv<br/>
Check this website for your OS to follow instructions if you had any problem<br/>
https://pipenv.pypa.io/en/latest/install/ <br/>
<br/>
Install pipenv on Mac with brew:<br/>
```
brew install pipenv
```
Install pipenv on Windows:<br/>
```
pip install pipenv
```<br/>
### Create your environment:<br/>
Note: after installing pipenv everything will be easier just open a terminal or command promt on the folder called "loginApp" where the "Pipfile" stored.
<br/>
After cd to loginApp<br/>
MacOS or Windows:
```
pipenv install
```
You can activate your environment but you don't have to<br/>
### Activate the environment in MacOS:<br/>
```
. <name of env>/bin/activate
```
### Activate the environment in Windows:<br/>
```
<name of env>\Scripts\activate
```
<br/>
Now your environment is ready now its time to setup db:<br/>
1- install docker desktop if you didn't from official website<br/>
2- cd into cs437 folder on your terminal or command prompt<br/>
3- test if docker is working with ```docker --version``` command<br/>
4- if you can see your version evderything is okay<br/>
5- just run te ```docker compose up``` command in the cs437 folder.<br/>
6- wait for 1-2 min anc you can shut down your terminal or press ctrl-C<br/>
7- now you will see your mongo container in Docker Desktop<br/>
8- install MongoDB Compass <br/>
9- use ```mongodb://admin:pass@localhost:27017/``` string to connect to mongodb<br/>
10- if this doesn't work try ```mongodb://localhost:27017/```<br/>
11- after connecting to your mongo instance create db from lest section and give the name "loginApp" and write "User" to collection name<br/>

note: on the initial run of app an instance called userEx will be added to db id doesn't exist<br/>

        user = {
            "username": "exUser",
            "password": generate_password_hash("123456789"),
            "email": "exUser@gmail.com",
            "recoveryPhrase": generate_password_hash("annemin kizlik soyadi")
        }

How to setup your flask app:<br/>
- One method is to cd to you "loginApp" folder, activate your venv, and run "python app.py" or "python3 app.py" command<br/>
<br/>
- Another method which I prefer is create a launch.json file if you're using VScode<br/>
- My example launch.json file in the .vscode folder but it is set for MacOS<br/>
- But by changing the ```"python": "${workspaceFolder}/loginApp/.venv/bin/python3.10"``` to your venv path it should work as well<br/>
- launch.json example<br/>
<img width="487" alt="Screen Shot 2022-12-19 at 16 56 27" src="https://user-images.githubusercontent.com/94080241/208441754-6aa75e98-1a1c-48db-97e7-7b664f688755.png">
<br/>
If I miss anything just reach me
