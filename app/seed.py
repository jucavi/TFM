from app import db
from app.auth.models import User
from app.project.models import Project, Team

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

def create_users():
    users = {}
    print('Populating users:')
    print(f'Password for all users: {PASSWORD!r}, you can change it later')

    for user in USERS.get('users', []):
        user = User(
            firstname=user.get('firstname'),
            lastname=user.get('lastname'),
            username=user.get('username'),
            email=user.get('email')
        )
        user.set_password(PASSWORD)
        users[user.username] = user

        print(f'User {user.username!r} created!')

    return users


# Each user has one project
def create_teams():
    teams = []
    users = create_users()
    for user in users.values():
        project = Project(
            project_name=f'Project of {user.username}',
            project_desc=f'Sample project with owner {user.username!r}'
        )

        print(f'Project {project!r} created!')
        teams.append(Team(project=project, user=user, is_owner=True))

    return teams

def seed():
    try:
        teams = create_teams()
        for team in teams:
            db.session.add(team)

        db.session.commit()
        print('All saved to database.')
    except Exception as e:
        print('Error:', e)

