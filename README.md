$ git clone https://github.com/jucavi/TFM.git

$ cd TFM

$ python3 -m venv .venv

$ source .venv/bin/activate

$ pip3 install -r requirements.txt

$ nano .env

		FLASK_APP=project
    		FLASK_ENV=development
    		SECRET_KEY=secret_key_here
    		MAIL_USERNAME=yourmail@gmail.com
   		MAIL_PASSWORD=your_password
    		MAIL_DEFAULT_SENDER=defaultmail@gmail.com

$flask db upgrade

if error: no folder versions found,
create 
		$ mkdir /migrations/versions



code <send_email>: https://j2logo.com/tutorial-flask-leccion-14-enviar-emails-con-flask/
