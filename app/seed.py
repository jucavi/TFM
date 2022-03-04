from app import db
from app.auth.user_model import User

PASSWORD = 'PA$$w0rd'

USERS = {
    'users': [
        {
            'firstname': 'Juan',
            'lastname': 'Vila',
            'username': 'juan',
            'email': 'juan@mailtrap.io'
        },
        {
            'firstname': 'Yoe',
            'lastname': 'Bilbao',
            'username': 'yoe',
            'email': 'yoe@mailtrap.io'
        },
        {
            'firstname': 'Raul',
            'lastname': 'Exposito',
            'username': 'raul',
            'email': 'raul@mailtrap.io'
        }
    ]

}


def users():
    for user in USERS.get('users', []):
        try:
            user = User(
                firstname=user.get('firstname'),
                lastname=user.get('lastname'),
                username=user.get('username'),
                email=user.get('email')
            )
            user.set_password(PASSWORD)

            db.session.add(user)
            db.session.commit()
            print(f'{user} created!')
        except Exception as e:
            print('Error:', e)