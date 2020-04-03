from getpass import getpass
import sys

from webapp import create_app
from webapp.model import db, User


app = create_app()

with app.app_context():
    username = input("Enter user name:")

    if User.query.filter(User.username == username).count():
        print("Username is already exist")
        sys.exit(0)

    password1 = getpass("Enter password")
    password2 = getpass("Repeat password")

    if not password1 == password2:
        print("Passwords do not match")
        sys.exit(0)

    new_user = User(username=username, role="admin")
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print("User has been created with id={}".format(new_user.id))