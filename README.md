# Tools for teams

Create your own team a share your data accessible for all team members.
[https://tfm-flask-tft.herokuapp.com](https://tfm-flask-tft.herokuapp.com)

## Usage

1. Clone repository
```bash
$ git clone https://github.com/jucavi/TFM.git
$ cd TFM
```

2. Create virtual enviroument and activate it
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```

3. Install dependencies
```bash
$ pip3 install -r requirements.txt
```

4.  Setup your environments variables
```bash
$ nano .env

FLASK_APP=project
FLASK_ENV=development
SECRET_KEY=secret_key_here
MAIL_USERNAME=yourmail@gmail.com
MAIL_PASSWORD=your_password
MAIL_DEFAULT_SENDER=defaultmail@gmail.com
```
Read [this](https://support.google.com/accounts/answer/185833?hl=en) before set MAIL_PASSWORD

5. Crete database
```bash
$ flask db upgrade
```

6. You can populate users for testing purposes
```bash
$ flask populate
```

7. Start server
```bash
$ flask run
```
