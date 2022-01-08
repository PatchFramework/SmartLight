import pandas as pd
from base64 import b64encode, b64decode

# for testing purposes only in clear text
passwords_clear = ["LightYagami", "ErenJaeger", "Dr.KenzoTenma"]

user_dict = {
    "name":     ["Canboi", "AKK", "Dom"],
    # encode the passwords with base64
    "password": [b64encode(s.encode("ascii")).decode("ascii") for s in passwords_clear]
    # the row number will be used as the user id
}
users = pd.DataFrame(user_dict)
users.rename_axis(index="id")

# save the users dataframe to a file (the row index of the df will be the user id)
users.to_csv("users.csv", index_label="id")

# print encoded passwords
print(user_dict["password"])

# print decoded passwords
decoded = [b64decode(s).decode("ascii") for s in user_dict["password"]]
print(decoded)