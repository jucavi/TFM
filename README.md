$ git clone https://github.com/jucavi/TFM.git
$ cd TFM

$ python3 -m venv .venv
$ pip3 install -r requirements.txt

$ nano .env
    add:
    SECRET_KEY='Your secret key here'
    FLASK_APP=project

$flask db upgrade
if error no folder versions found, create create /migrations/versions folder



send_email: https://j2logo.com/tutorial-flask-leccion-14-enviar-emails-con-flask/
