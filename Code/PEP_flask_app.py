from flask import Flask, request, jsonify
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from DB_Operations import Database

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "cibcproject"
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    """
    This function handles the login process. It expects a POST request with a JSON body containing 'employeeID' and 'password'.
    The function checks the provided employeeID and password against the database.

    If the employeeID is not found in the database, it returns a JSON response with a message "Invalid employee ID" and a code 1002.

    If the employeeID is found, it checks the login count. If the login count is 0, it means the user is logging in for the first time.
    In this case, the function checks if the provided password matches the user's DOB (which is the default password).
    If the password matches, it returns a JSON response with a message "Redirect to create new password" and a code 1000.

    If the login count is not 0, it means the user has logged in before and has set a custom password.
    In this case, the function checks if the provided password matches the stored hash of the user's custom password.
    If the password matches, it increments the login count, generates a JWT token, and returns a JSON response with a message "Login successful", a code 0, and the JWT token.
    The JWT token should be stored on the client side and included in the Authorization header in subsequent requests.
    If the password does not match at any point, it returns a JSON response with a message "Invalid password" and a code 1001.
    """
    data = request.get_json()

    employeeID = data["employeeID"]
    password = data["password"]

    db = Database("Employees")
    result = db.query("SELECT * FROM Password WHERE employeeID=%s", (employeeID,))

    if result:
        stored_employeeID = result[0]["employeeID"]
        stored_hash = result[0]["PasswordHash"]
        login_count = result[0]["loginCount"]

        # if login count is 0, check if password is the same as default (DOB)
        if login_count == 0:
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                return jsonify(message="Redirect to create new password", code=1000), 200
            else:
                return jsonify(message="Invalid password", code=1001), 401

        # if login count is not 0, check password against stored hash
        elif bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            # if the login is successful, create a JWT token and increment login count
            access_token = create_access_token(identity=stored_employeeID)
            db.query("UPDATE Password SET loginCount = loginCount + 1 WHERE employeeID=%s", (employeeID,))
            return jsonify(message="Login successful", code=0, token=access_token), 200
        else:
            return jsonify(message="Invalid password", code=1001), 401
    else:
        return jsonify(message="Invalid employee ID", code=1002), 401
    db.con.close()


@app.route("/set_password", methods=["POST"])
@jwt_required()
def set_password():
    """
    This function handles the password setting process. It expects a POST request with a JSON body containing 'oldPassword', and 'newPassword'.

    The function requires the user's JWT token in the 'Authorization' header of the request.

    The function checks the provided oldPassword against the database.

    If the oldPassword does not match the stored hash, it returns a JSON response with a message "Invalid old password" and a code 1001.

    If the oldPassword matches, it hashes the newPassword and updates the stored hash in the database, then returns a JSON response with a message "Password updated successfully" and a code 0.
    """
    data = request.get_json()

    oldPassword = data["oldPassword"]
    newPassword = data["newPassword"]

    # get the employeeID from the JWT token
    employeeID = get_jwt_identity()

    db = Database("Employees")
    result = db.query("SELECT * FROM Password WHERE employeeID=%s", (employeeID,))

    if result:
        stored_hash = result[0]["PasswordHash"]

        # check if oldPassword  matches stored hash
        if bcrypt.checkpw(oldPassword.encode('utf-8'), stored_hash.encode('utf-8')):
            # if the oldPassword is correct, salt and hash the newPassword and update the database
            salt = bcrypt.gensalt()
            new_hash = bcrypt.hashpw(newPassword.encode('utf-8'), salt)
            db.query("UPDATE Password SET PasswordHash = %s WHERE employeeID = %s", (new_hash, employeeID))
            return jsonify(message="Password updated successfully", code=0), 200
        else:
            return jsonify(message="Invalid old password", code=1001), 401
    else:
        return jsonify(message="Invalid employee ID", code=1002), 401
    db.con.close()


if __name__ == "__main__":
    app.run(debug=True)
