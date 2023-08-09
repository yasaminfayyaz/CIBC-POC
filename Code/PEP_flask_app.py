from flask import Flask, request, jsonify
import bcrypt
import sys
import JSON
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from utils import indoorLocation
from booleanChecks import *


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "cibcproject"
jwt = JWTManager(app)




@app.route("/", methods=["POST"])
@jwt_required()

def access_request():
    from pyxacml_sdk.core import sdk
    from pyxacml_sdk.model.attribute import Attribute
    from pyxacml_sdk.model.attribute_ids import Attribute_ID
    from pyxacml_sdk.model.categories import Category_ID
    from pyxacml_sdk.model.datatypes import Datatype
    from DB_Operations import Database

    try:

        data = request.get_json()

        employeeID = get_jwt_identity()

        #TODO: ASK FELIPE TO INCLUDE THESE IN THE REQUEST
        resourceID = data["ResourceID"]

        actionID = data["ActionID"]



        sdk = sdk.Sdk(
                # Path to our configuration file
                "config.yml",
                # Domain ID
                "oUVpvyqyEe6P-AZjTGYSFQ")

        #Building XACML attributes using the data from the request, derived, and stored attributes


        #Dyanmic attributes

        app_safety_status = Attribute(Attribute_ID.INSTALLED_APPS_SAFE, areInstalledAppsSafe(data["installedApps"]), Datatype.BOOLEAN)
        at_primary_branch = Attribute(Attribute_ID.AT_PRIMARY_BRANCH, isAtPrimaryBranch(employeeID, data["CurrentLocationCoords"]["latitude"], data["CurrentLocationCoords"]["longitude"]), Datatype.BOOLEAN)
        location_trusted = Attribute(Attribute_ID.LOCATION_TRUSTED, isAtTrustedLocation(employeeID), Datatype.BOOLEAN)
        #TODO: CONFIRM UNIQUEID IS THE DEVICE IDENTIFIER
        device_registered = Attribute(Attribute_ID.DEVICE_REGISTERED, isRegisteredDevice(employeeID, data["DeviceInfo"]["uniqueId"]), Datatype.BOOLEAN)
        work_hours = Attribute(Attribute_ID.WORK_HOURS, isWorkHours(), Datatype.BOOLEAN)
        #Is clearance of those around same or higher than the employee?
        sufficient_clearnace = Attribute(Attribute_ID.SUFFICIENT_CLEARANCE, isClearanceSufficient(employeeID), Datatype.BOOLEAN)
        redflags =  data["CurrentLocation"]["mocked"] or not data["DeviceInfo"]["pinOrFingerprintSet"] or \
                           data["DeviceInfo"]["emulator"] or isDeviceBrandUnsafe(data["DeviceInfo"]["brand"])
        #Are there any red flags with the device?
        device_redflags = Attribute(Attribute_ID.DEVICE_REDFLAGS, redflags, Datatype.BOOLEAN)
        #TODO: GET CURRENT CLEARNACE

        #Static employee attributes
        db_employee = Database("Employees")
        department = db_employee.query("SELECT department FROM Employee WHERE employeeID = %s", (employeeID,))[0]["department"]
        employee_department = Attribute(Attribute_ID.EMPLOYEE_DEPARTMENT, department, Datatype.STRING)
        initial_clearance = db_employee.query("SELECT initSecClearance FROM Employee WHERE employeeID = %s", (employeeID,))[0]["initSecClearance"]
        employee_initial_clearance = Attribute(Attribute_ID.EMPLOYEE_INIT_CLEARANCE, initial_clearance, Datatype.STRING)
        db_employee.con.close()

        #Resource attributes
        db_resource = Database("Resources")
        department = db_resource.query("SELECT department FROM Resource WHERE resourceID = %s", (resourceID,))[0]["department"]
        resource_department = Attribute(Attribute_ID.RESOURCE_DEPARTMENT, department, Datatype.STRING)
        type = db_resource.query("SELECT resourceType FROM Resource WHERE resourceID = %s", (resourceID,))[0]["resourceType"]
        resource_type = Attribute(Attribute_ID.RESOURCE_TYPE, type, Datatype.STRING)
        security_level = db_resource.query("SELECT secLevel FROM Resource WHERE resourceID = %s", (resourceID,))[0]["secLevel"]
        resource_security_level = Attribute(Attribute_ID.RESOURCE_SEC_LEVEL, security_level, Datatype.STRING)
        db_resource.con.close()

        #Action attributes
        action_id = Attribute(Attribute_ID.ACTION_ID, actionID, Datatype.STRING)


        # Adding attributes to our request
        sdk.add_attribute(Category_ID.REQUESTING_MACHINE, app_safety_status)
        sdk.add_attribute(Category_ID.ACCESS_SUBJECT, at_primary_branch)
        sdk.add_attribute(Category_ID.ACCESS_SUBJECT, location_trusted)
        sdk.add_attribute(Category_ID.REQUESTING_MACHINE, device_registered)
        sdk.add_attribute(Category_ID.ENVIRONMENT, work_hours)
        sdk.add_attribute(Category_ID.ACCESS_SUBJECT, sufficient_clearnace)
        sdk.add_attribute(Category_ID.REQUESTING_MACHINE, device_redflags)
        sdk.add_attribute(Category_ID.ACCESS_SUBJECT, employee_department)
        sdk.add_attribute(Category_ID.ACCESS_SUBJECT, employee_initial_clearance)
        sdk.add_attribute(Category_ID.RESOURCE, resource_department)
        sdk.add_attribute(Category_ID.RESOURCE, resource_type)
        sdk.add_attribute(Category_ID.RESOURCE, resource_security_level)
        sdk.add_attribute(Category_ID.ACTION, action_id)

        # Asking for Authorization
        decision, raw = sdk.get_authz()

        #Communicating the decision to the client
        if decision == "Permit":
            return jsonify({"message": "Access granted", "code": 1000}), 200
        elif decision == "Deny":
            return jsonify({"message": "Access denied", "code": 1001}), 403

        else:
            return jsonify({"message": "Error", "code": 1002}), 500

    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {str(e)}", "code": 1003}), 500


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
                access_token = create_access_token(identity=stored_employeeID)
                return jsonify(message="Redirect to create new password", code=1000, token=access_token), 200
            else:
                return jsonify(message="Invalid password", code=1001), 401

        # if login count is not 0, check password against stored hash
        elif bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            db.query("UPDATE Password SET loginCount = loginCount + 1 WHERE employeeID=%s", (employeeID,))
            return jsonify(message="Login successful", code=0), 200
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

@app.route("/get_resources", methods=["GET"])
@jwt_required()
def get_resources():
    """
    This function handles the retrieval of resources that the employee can see (not necessarily access) based on their initial security clearance.
    The function requires the employee's JWT token in the 'Authorization' header of the request.

    The function retrieves the employee's initial security clearance from the Employee database, then retrieves all resources from the Resource database that have a security level that is the same or lower than the employee's initial security clearance.

    The function returns a JSON response with a list of resources. Each resource is represented as a dictionary with 'resourceID' and 'resourceName'.
    """
    employeeID = get_jwt_identity()

    db_employee = Database("Employees")
    result_employee = db_employee.query("SELECT initSecClearance FROM Employee WHERE employeeID=%s", (employeeID,))
    initSecClearance = result_employee[0]["initSecClearance"]

    # map security levels to numerical values
    sec_levels = {"Unclassified": 0, "Restricted": 1, "Confidential": 2, "Secret": 3, "Top Secret": 4}
    initSecClearance_value = sec_levels[initSecClearance]

    db_resource = Database("Resources")
    result_resource = db_resource.query("SELECT resourceID, resourceName, secLevel FROM Resource")

    # create a list of resources that the employee can see
    resources = [{"resourceID": resource["resourceID"], "resourceName": resource["resourceName"]} for resource in result_resource if sec_levels[resource["secLevel"]] <= initSecClearance_value]

    db_employee.con.close()
    db_resource.con.close()

    return jsonify(resources=resources), 200


@app.route('/update_location', methods=['POST'])
@jwt_required
def update_location():
    """
    This function updates the location of an employee based on the RSSI values received from the client.

    The client should send a POST request with a JSON body containing two fields:
    - 'BSSIDs': a list of BSSID strings corresponding to the 3 Wi-Fi access points.
    - 'RSSIs': a list of RSSI values corresponding to the BSSIDs. The RSSI values should be in the same order as the BSSIDs.

    The client should also include the JWT token in the 'Authorization' header of the request.

    Example request body:
    {
        "BSSIDs": ["00:0a:95:9d:68:16", "00:0a:95:9d:68:17", "00:0a:95:9d:68:18"],
        "RSSIs": [-50, -60, -70]
    }

    The function will update the location of the employee in the database based on the RSSI values and return a JSON response with a message "Location updated".

    If an error occurs, the function will return a JSON response with an error message.
    """
    BSSIDs = request.json.get('BSSIDs', None)
    RSSIs = request.json.get('RSSIs', None)
    employeeID = get_jwt_identity()  # Get the employee id from the JWT
    indoorLocation(BSSIDs, RSSIs, employeeID)
    return jsonify({"msg": "Location updated"}), 200



@app.route('/get_bssids', methods=['GET'])
def get_bssids():
    """
    This endpoint retrieves all BSSIDs associated with APs of interest from the database and returns them in a JSON format.

    The returned JSON object is an array of dictionaries, where each dictionary represents a row from the AP table. Each dictionary has a single key-value pair, where the key is 'BSSID' and the value is the BSSID of an access point.

    Example response:
    [
        {"BSSID": "00:0a:95:9d:68:16"},
        {"BSSID": "00:0a:95:9d:68:17"},
        {"BSSID": "00:0a:95:9d:68:18"}
    ]

    """
    db = Database("LocationReference")
    bssids = db.query("SELECT BSSID FROM AP")
    db.con.close()
    return jsonify(bssids)




if __name__ == "__main__":
    app.run(debug=True)
