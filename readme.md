## About Project 13
- This deposit concerns the project number 13 of openclassrooms that you can find below the instruction for the installation and the necessary information

- URL HEROKU In progress

## For installation
#### In your terminal : 
* Create a python environment : 
    * `$ pip install virtualenv `
    * `$ virtualenv -p python3 venv` 
    * `$ activate venv` 
* Clone this repository on the same folder with venv
* Install requirements :
    * `$ pip install -r requirements.txt`
    * install https://www.postgresql.org/ on your os
        * Make data base :
            *   'NAME': 'chess_platform'
            *   'USER': 'anthony'
            *   'PASSWORD': 'YOUR_PASSWORD' EDIT PASSWORD in free_chess_gui\settings.py 103
            *   'HOST': '127.0.0.1'
            *   'PORT': '5432'
* In your terminal go to the root of the repository, then enter :
    * `$ activate venv` 
    * `$ python manage.py migrate`
    * `$ python manage.py runserver`
    * `$ python manage.py run_chat_server`

* Go to  http://127.0.0.1:8000/

## Functionality
* You can play a game against the best computers chess in the world
* you can launch an analysis of your games or of a game you want to import with the three best computers chess in the world
    * lc0
    * stockfish NNUE
    * komodo
## Example

![](https://github.com/Anthony10700/P13/blob/master/img_screen/1.PNG?raw=true)
![](https://github.com/Anthony10700/P13/blob/master/img_screen/2.PNG?raw=true)
