# Tools for teams

Create your own team a share your data accessible for all team members.

## Usage

1. Clone repository

        $ git clone https://github.com/jucavi/TFM.git
        $ cd TFM

2. Create virtual enviroument and activate it

        $ python3 -m venv .venv
        $ source .venv/bin/activate

3. Install dependencies

        $ pip3 install -r requirements.txt

4.  Setup your environments variables

        $ nano .env

		FLASK_APP=project
    	FLASK_ENV=development
    	SECRET_KEY=secret_key_here
    	MAIL_USERNAME=yourmail@gmail.com
   		MAIL_PASSWORD=your_password
    	MAIL_DEFAULT_SENDER=defaultmail@gmail.com

    Read [this](https://support.google.com/accounts/answer/185833?hl=en) before set MAIL_PASSWORD

5. Crete database

        $ flask db upgrade

6. Start server

        $ flask run
