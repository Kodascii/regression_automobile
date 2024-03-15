from app import app, db
from app.models import User

app.app_context().push()

# Get all users
users = User.query.all()

# Print the usernames and isAdmin status of all users
for user in users:
    print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, isAdmin: {user.isAdmin}")

