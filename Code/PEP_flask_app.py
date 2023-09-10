from flask import Flask, request, jsonify
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from utils import indoorLocation, stringSecLabel_to_int, get_base_rate, update_base_rate
from booleanChecks import areInstalledAppsSafe, isAtPrimaryBranch, isAtTrustedLocation, isRegisteredDevice, isWorkHours, isClearanceSufficient, isDeviceBrandUnsafe, wasAppJustInstalled
from trustEngine import build_quadruple, currentClearance
from pyxacml_sdk.core import sdk
from pyxacml_sdk.model.attribute import Attribute
from pyxacml_sdk.model.attribute_ids import Attribute_ID
from pyxacml_sdk.model.categories import Category_ID
from pyxacml_sdk.model.datatypes import Datatype
from DB_Operations import Database

# Relative path to configuration file
config_file_path = "/home/Yafa/CIBC-POC/Code/config.yml"

# Domain ID
domain_id = "A0bdIbmGEeWhFwcKrC9gSQ"

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "cibcproject"
jwt = JWTManager(app)



# Initialize the SDK with the loaded configuration and domain ID
sdk = sdk.Sdk(config_file_path, domain_id)

@app.route("/", methods=["POST"])
@jwt_required()
def access_request():
    try:
        data = request.get_json()
        employeeID = get_jwt_identity()
        resourceID = data["ResourceID"]
        actionID = data["ActionID"]

        # Building + adding XACML attributes using the data from the request, derived, and stored attributes

        # Dynamic attributes
        # Weights for each attribute, used to calculate the trust score
        quadruples = []
        weights = {
            "INSTALLED_APPS_SAFE": 0.9,
            "AT_PRIMARY_BRANCH": 0.8,
            "LOCATION_TRUSTED": 0.7,
            "DEVICE_REGISTERED": 1,
            "WORK_HOURS": 0.5,
            "SUFFICIENT_CLEARANCE": 0.8,
            "NOT_EMULATOR": 1,
            "LOCATION_NOT_MOCKED": 1,
            "BRAND_SAFE": 0.8,
            "PIN_OR_FINGERPRINT_SET": 1,
            "APP_NOT_JUST_INSTALLED": 0.5
        }
        try:
            # Checks if any of the installed apps on the employee's phone are blacklisted due to potential security risks

            INSTALLED_APPS_SAFE = areInstalledAppsSafe(data["installedApps"])
            app_safety_status = Attribute(Attribute_ID.INSTALLED_APPS_SAFE, INSTALLED_APPS_SAFE, Datatype.BOOLEAN)
            sdk.add_attribute(Category_ID.subjectCat, app_safety_status)

            # Pass to trust engine
            quadruples.append(build_quadruple(INSTALLED_APPS_SAFE, weights["INSTALLED_APPS_SAFE"], get_base_rate("INSTALLED_APPS_SAFE")))
            update_base_rate(employeeID, "INSTALLED_APPS_SAFE", INSTALLED_APPS_SAFE)
        except:
            quadruples.append(build_quadruple(None, weights["INSTALLED_APPS_SAFE"], get_base_rate("INSTALLED_APPS_SAFE")))

        try:
            # Checks if the employee is at their primary branch
            AT_PRIMARY_BRANCH = isAtPrimaryBranch(employeeID, data["CurrentLocationCoords"]["latitude"], data["CurrentLocationCoords"]["longitude"])
            at_primary_branch = Attribute(Attribute_ID.AT_PRIMARY_BRANCH, AT_PRIMARY_BRANCH, Datatype.BOOLEAN)
            sdk.add_attribute(Category_ID.subjectCat, at_primary_branch)

            # Pass to trust engine
            quadruples.append(build_quadruple(AT_PRIMARY_BRANCH, weights["AT_PRIMARY_BRANCH"], get_base_rate("AT_PRIMARY_BRANCH")))
            update_base_rate(employeeID, "AT_PRIMARY_BRANCH", AT_PRIMARY_BRANCH)
        except:
            quadruples.append(
                build_quadruple(None, weights["AT_PRIMARY_BRANCH"], get_base_rate("AT_PRIMARY_BRANCH")))

        try:
            # Checks if the employee is at a trusted location
            LOCATION_TRUSTED = isAtTrustedLocation(employeeID)
            location_trusted = Attribute(Attribute_ID.LOCATION_TRUSTED, LOCATION_TRUSTED, Datatype.BOOLEAN)
            sdk.add_attribute(Category_ID.subjectCat, location_trusted)

            # Pass to trust engine
            quadruples.append(build_quadruple(LOCATION_TRUSTED, weights["LOCATION_TRUSTED"], get_base_rate("LOCATION_TRUSTED")))
            update_base_rate(employeeID, "LOCATION_TRUSTED", LOCATION_TRUSTED)
        except:
            quadruples.append(build_quadruple(None, weights["LOCATION_TRUSTED"], get_base_rate("LOCATION_TRUSTED")))

        try:
            # Checks if the employee's device is registered
            DEVICE_REGISTERED = isRegisteredDevice(employeeID, data["DeviceInfo"]["uniqueId"])

            device_registered = Attribute(Attribute_ID.DEVICE_REGISTERED, DEVICE_REGISTERED, Datatype.BOOLEAN)
            sdk.add_attribute(Category_ID.subjectCat, device_registered)

            # Pass to trust engine
            quadruples.append(build_quadruple(DEVICE_REGISTERED, weights["DEVICE_REGISTERED"], get_base_rate("DEVICE_REGISTERED")))
            update_base_rate(employeeID, "DEVICE_REGISTERED", DEVICE_REGISTERED)
        except:
            quadruples.append(
            build_quadruple(None, weights["DEVICE_REGISTERED"], get_base_rate("DEVICE_REGISTERED")))

        try:
            # Checks if the employee is making the access request during work hours
            WORK_HOURS = isWorkHours()
            work_hours = Attribute(Attribute_ID.WORK_HOURS, WORK_HOURS, Datatype.BOOLEAN)
            sdk.add_attribute(Category_ID.environmentCat, work_hours)

            # Pass to trust engine
            quadruples.append(build_quadruple(WORK_HOURS, weights["WORK_HOURS"], get_base_rate("WORK_HOURS")))
            update_base_rate(employeeID, "WORK_HOURS", WORK_HOURS)
        except:
            quadruples.append(build_quadruple(None, weights["WORK_HOURS"], get_base_rate("WORK_HOURS")))

        try:
            # Check to see if employees in the same indoor location as the one making access requests have equal or higher clearance
            SUFFICIENT_CLEARANCE = isClearanceSufficient(employeeID)
            sufficient_clearance = Attribute(Attribute_ID.SUFFICIENT_CLEARANCE, SUFFICIENT_CLEARANCE, Datatype.BOOLEAN)
            sdk.add_attribute(Category_ID.subjectCat, sufficient_clearance)

            # Pass to trust engine
            quadruples.append(build_quadruple(SUFFICIENT_CLEARANCE, weights["SUFFICIENT_CLEARANCE"], get_base_rate("SUFFICIENT_CLEARANCE")))
            update_base_rate(employeeID, "SUFFICIENT_CLEARANCE", SUFFICIENT_CLEARANCE)
        except:
            sufficient_clearance_exists = Attribute(Attribute_ID.SUFFICIENT_CLEARANCE_EXISTS, False, Datatype.BOOLEAN)
            sdk.add_attribute(Category_ID.subjectCat, sufficient_clearance_exists)

        try:
            # Checks if the employee's device is a known emulator or has a known unsafe brand, etc.
            redflags = data["CurrentLocation"]["mocked"] or not data["DeviceInfo"]["pinOrFingerprintSet"] or data["DeviceInfo"]["emulator"] or isDeviceBrandUnsafe(data["DeviceInfo"]["brand"])
            device_redflags = Attribute(Attribute_ID.DEVICE_REDFLAGS, redflags, Datatype.BOOLEAN)
            sdk.add_attribute(Category_ID.subjectCat, device_redflags)

            # Pass to trust engine
            LOCATION_NOT_MOCKED = not data["CurrentLocation"]["mocked"]
            NOT_EMULATOR = not data["DeviceInfo"]["emulator"]
            BRAND_SAFE = not isDeviceBrandUnsafe(data["DeviceInfo"]["brand"])
            PIN_OR_FINGERPRINT_SET = data["DeviceInfo"]["pinOrFingerprintSet"]

            quadruples.append(build_quadruple(LOCATION_NOT_MOCKED, weights["LOCATION_NOT_MOCKED"], get_base_rate("LOCATION_NOT_MOCKED")))
            quadruples.append(build_quadruple(NOT_EMULATOR, weights["NOT_EMULATOR"], get_base_rate("NOT_EMULATOR")))
            quadruples.append(build_quadruple(BRAND_SAFE, weights["BRAND_SAFE"], get_base_rate("BRAND_SAFE")))
            quadruples.append(build_quadruple(PIN_OR_FINGERPRINT_SET, weights["PIN_OR_FINGERPRINT_SET"], get_base_rate("PIN_OR_FINGERPRINT_SET")))

            update_base_rate(employeeID, "LOCATION_NOT_MOCKED", LOCATION_NOT_MOCKED)
            update_base_rate(employeeID, "NOT_EMULATOR", NOT_EMULATOR)
            update_base_rate(employeeID, "BRAND_SAFE", BRAND_SAFE)
            update_base_rate(employeeID, "PIN_OR_FINGERPRINT_SET", PIN_OR_FINGERPRINT_SET)
        except:
            quadruples.append(build_quadruple(None, weights["LOCATION_NOT_MOCKED"], get_base_rate("LOCATION_NOT_MOCKED")))
            quadruples.append(build_quadruple(None, weights["NOT_EMULATOR"], get_base_rate("NOT_EMULATOR")))
            quadruples.append(build_quadruple(None, weights["BRAND_SAFE"], get_base_rate("BRAND_SAFE")))
            quadruples.append(build_quadruple(None, weights["PIN_OR_FINGERPRINT_SET"], get_base_rate("PIN_OR_FINGERPRINT_SET")))



        try:
            APP_NOT_JUST_INSTALLED = not wasAppJustInstalled(data["DeviceInfo"]["firstInstallTime"])
            quadruples.append(build_quadruple(APP_NOT_JUST_INSTALLED, weights["APP_NOT_JUST_INSTALLED"], get_base_rate("APP_NOT_JUST_INSTALLED")))
            update_base_rate(employeeID, "APP_NOT_JUST_INSTALLED", APP_NOT_JUST_INSTALLED)
        except:
            quadruples.append(None, weights["APP_NOT_JUST_INSTALLED"], get_base_rate("APP_NOT_JUST_INSTALLED"))

        try:
            # Employee's current clearance which be dynamically updated based on trust score, possible values: {Top Secret, Secret, Confidential, Restricted, Unclassified}
            employee_current_clearance = Attribute(Attribute_ID.EMPLOYEE_CURRENT_CLEARANCE, stringSecLabel_to_int(currentClearance(quadruples)), Datatype.INTEGER)
            sdk.add_attribute(Category_ID.subjectCat, employee_current_clearance)
        except:
            pass

        # Static employee attributes
        try:
            db_employee = Database("Employees")
            # Possible values: {Customer Service, Accounting, Risk Management, Loan Processing, Mortgage Services, Investment Banking, Compliance, Human Resources, Information Technology, Marketing}
            department = db_employee.query("SELECT department FROM Employee WHERE employeeID = %s", (employeeID,))[0]["department"]
            employee_department = Attribute(Attribute_ID.EMPLOYEE_DEPARTMENT, department, Datatype.STRING)
            sdk.add_attribute(Category_ID.subjectCat, employee_department)



            # Possible values: {Top Secret: 5, Secret: 4, Confidential: 3, Restricted: 2, Unclassified: 1}
            initial_clearance = db_employee.query("SELECT initSecClearance FROM Employee WHERE employeeID = %s", (employeeID,))[0]["initSecClearance"]
            employee_initial_clearance = Attribute(Attribute_ID.EMPLOYEE_INIT_CLEARANCE, stringSecLabel_to_int(initial_clearance), Datatype.INTEGER)
            sdk.add_attribute(Category_ID.subjectCat, employee_initial_clearance)
            db_employee.con.close()
        except:
            pass

        # Resource attributes
        try:
            db_resource = Database("Resources")
            # Possible values: {Customer Service, Accounting, Risk Management, Loan Processing, Mortgage Services, Investment Banking, Compliance, Human Resources, Information Technology, Marketing}
            department = db_resource.query("SELECT department FROM Resource WHERE resourceID = %s", (resourceID,))[0]["department"]
            resource_department = Attribute(Attribute_ID.RESOURCE_DEPARTMENT, department, Datatype.STRING)
            sdk.add_attribute(Category_ID.resourceCat, resource_department)
            # Possible values: {Records, Archives, Documents, Artifacts, Information Assets, Intellectual Property, Research Materials}
            type = db_resource.query("SELECT resourceType FROM Resource WHERE resourceID = %s", (resourceID,))[0]["resourceType"]
            resource_type = Attribute(Attribute_ID.RESOURCE_TYPE, type, Datatype.STRING)
            sdk.add_attribute(Category_ID.resourceCat, resource_type)


            # Possible values: {Top Secret: 5, Secret: 4, Confidential: 3, Restricted: 2, Unclassified: 1}
            security_level = db_resource.query("SELECT secLevel FROM Resource WHERE resourceID = %s", (resourceID,))[0]["secLevel"]
            resource_security_level = Attribute(Attribute_ID.RESOURCE_SEC_LEVEL, stringSecLabel_to_int(security_level), Datatype.INTEGER)
            sdk.add_attribute(Category_ID.resourceCat, resource_security_level)
            db_resource.con.close()
        except:
            pass

        # Action attributes
        try:
            action_id = Attribute(Attribute_ID.ACTION_ID, actionID, Datatype.STRING)
            sdk.add_attribute(Category_ID.actionCat, action_id)
        except:
            pass




        # Asking for Authorization
        decision, raw = sdk.get_authz()

        # Communicating the decision to the client
        if decision == "Permit":
            return jsonify({"message": "Access granted", "code": 1000}), 200
        elif decision == "Deny":
            return jsonify({"message": "Access denied", "code": 1001}), 403
        elif decision == "Indeterminate":
            return jsonify({"message": "Access denied: INSUFFICIENT INFORMATION!", "code": 1002}), 403
        else:
            return jsonify({"message": "Error", "code": 1003}), 500

    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {str(e)}", "code": 1004}), 500

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
            db.query("UPDATE Password SET loginCount = loginCount + 1 WHERE employeeID=%s", (employeeID,))
            access_token = create_access_token(identity=stored_employeeID)
            return jsonify(message="Login successful", code=0, token=access_token), 200
        else:
            return jsonify(message="Invalid password", code=1001), 401
    else:
        return jsonify(message="Invalid employee ID", code=1002), 401
    db.con.close()


# This route is no longer protected
@app.route("/set_password", methods=["POST"])
def set_password():
    """
    This function handles the password setting process. It expects a POST request with a JSON body containing 'employeeID', 'oldPassword', and 'newPassword'.

    The function checks the provided oldPassword against the database.

    If the oldPassword does not match the stored hash, it returns a JSON response with a message "Invalid old password" and a code 1001.

    If the oldPassword matches, it hashes the newPassword and updates the stored hash in the database, then returns a JSON response with a message "Password updated successfully" and a code 0.
    """
    data = request.get_json()

    # get the employeeID from the request body
    employeeID = data["employeeID"]
    oldPassword = data["oldPassword"]
    newPassword = data["newPassword"]

    db = Database("Employees")
    result = db.query("SELECT * FROM Password WHERE employeeID=%s", (employeeID,))

    if result:
        stored_hash = result[0]["PasswordHash"]
        login_count = result[0]["loginCount"]

        # check if oldPassword  matches stored hash
        if bcrypt.checkpw(oldPassword.encode('utf-8'), stored_hash.encode('utf-8')):
            # if the oldPassword is correct, salt and hash the newPassword and update the database
            salt = bcrypt.gensalt()
            new_hash = bcrypt.hashpw(newPassword.encode('utf-8'), salt)

            if login_count != 0:
                db.insert("UPDATE Password SET PasswordHash = %s WHERE employeeID = %s", (new_hash, employeeID))
            else:
                db.insert("UPDATE Password SET PasswordHash = %s, loginCount = %s + 1 WHERE employeeID = %s", (new_hash, login_count, employeeID))

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
    app.run(debug=True, port=5001)
