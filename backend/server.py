from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import os
from base64 import b64encode, b64decode
import pandas as pd

# to generate a random password
import random
import string

def generate_secret_file(file=".secret"):
    """
    Creates a random password for the API server. This is not related to user passwords.
    The random password will be saved in clear text to 'secret_clear.txt' if you run the server for the first time.
    """
    # skip if it already exists
    if os.path.isfile(file):
        return
    
    # 8 to 15 random ascii letters
    random_chars = [random.choice(string.ascii_letters) 
            for _ in range(random.randint(8,15))]

    secret = "".join(random_chars)
    
    os.environ["S_TMP"] = secret

    print(
"You can view your API secret in the file secret_clear.txt\
make sure to delete it after you read it."
)
    
    # write the secret to the "file"
    with open("secret_clear.txt", "x") as f:
        f.write(secret)
    
    with open(file, "x") as f: 
        secret = f"{secret}".encode("utf-8")
        encoded_sec = b64encode(secret)
        f.write(str(encoded_sec))
    return


class User(object):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

    # def __str__(self):
    #     return f"User(id={self.id})"

# read in the user data from the user file
user_file = "users.csv"
global users
if os.path.isfile(user_file):
    users = pd.read_csv(user_file)

print(users)

def user_object_from_df(name=None, id=None):
    """
    Creates an instance of the User() class for an entry in the dataframe that has the provided username or id.  
    """
    # getting the user from the dataframe
    try:
        if name and not id:
            user = users[users["name"] == name]
        elif not name and id:
            user = users[users["id"] == id]
    except:
        print("This user is not in the database")
        return None
    # reading the information from the user
    try:
        return User(user["id"], user["name"], user["password"])
    except:
        print("Couldn't read the user data from the dataframe")
        return None


def authenticate(username, password):
    user = user_object_from_df(name=username)
    # compare the base64 encoded passwords
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return user_object_from_df(id=user_id)


app = Flask(__name__)
app.debug = True
# set the password for the REST API Server
try:
    generate_secret_file() # will only create a file if it doesn't exist already
    with open(".secret", "r") as f:
        encoded = f.read()
        decoded = b64decode(encoded).encode("ascii")
        print("secret", encoded, decoded)
        app.config['SECRET_KEY'] = decoded
except:
    print("There is no '.secret' file in the current directory, will not start the server without a password.")

jwt = JWT(app, authenticate, identity)


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


if __name__ == '__main__':
    app.run()

