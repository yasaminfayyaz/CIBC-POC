from geopy.distance import geodesic
from DB_Operations import Database
from datetime import datetime

def isAtPrimaryBranch(employeeID, currentLat, currentLong):
    try:
        db = Database("Employees")
        radius = 0.1
        primaryBranchID = db.query("SELECT primaryBranchID FROM Employee WHERE employeeID = %s", (employeeID,))[0]["primaryBranchID"]
        branchLocation = db.query("SELECT latitude, longitude FROM Branch WHERE branchID = %s", (primaryBranchID,))[0]
        branchLat = branchLocation["latitude"]
        branchLong = branchLocation["longitude"]
        # Calculate the distance between the current location and the branch location
        distance = geodesic((currentLat, currentLong), (branchLat, branchLong)).kilometers
        # Compare the distance with the radius
        return distance <= radius
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
    finally:
        db.con.close()

def isAtTrustedLocation(employeeID):
    try:
        db_employee = Database("Employees")
        locationID = db_employee.query("SELECT locationID FROM EmployeeLocation WHERE employeeID = %s", (employeeID,))[0]["locationID"]

        db_location = Database("LocationReference")
        isTrusted = db_location.query("SELECT isTrusted FROM Location WHERE locationID = %s", (locationID,))[0]["isTrusted"]
        return bool(isTrusted)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
    finally:
        db_employee.con.close()
        db_location.con.close()


def isRegisteredDevice(employeeID, currentDeviceID):
    try:
        db = Database("Employees")
        registeredDeviceID = db.query("SELECT deviceID FROM Device WHERE employeeID = %s", (employeeID,))
        if registeredDeviceID:
            return registeredDeviceID[0]["deviceID"] == currentDeviceID
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e

    finally:
        db.con.close()


def isWorkHours():
    now = datetime.now()

    # Check if today is a weekday (0 = Monday, 6 = Sunday)
    if now.weekday() >= 5:  # If it"s Saturday or Sunday
        return False

    # Define work hours start and end
    work_Hours_Start = now.replace(hour=8, minute=0, second=0, microsecond=0)
    work_Hours_End = now.replace(hour=18, minute=0, second=0, microsecond=0)


    if work_Hours_Start <= now <= work_Hours_End:
        return True
    else:
        return False

def isClearanceSufficient(employeeID):
    try:
        db = Database("Employees")
        clearanceRanking = {"Unclassified": 0, "Restricted": 1, "Confidential": 2, "Secret": 3, "Top Secret": 4}

        # Get the security clearance of the given employee
        employeeSecLevel = db.query("SELECT initSecClearance FROM Employee WHERE employeeID = %s", (employeeID,))[0]["initSecClearance"]
        employeeSecLevel_value = clearanceRanking[employeeSecLevel]

        # Get the location of the given employee
        employeeLocation = db.query("SELECT locationID FROM EmployeeLocation WHERE employeeID = %s", (employeeID,))[0]["locationID"]

        # Get the security clearances of all other employees in the same location
        otherEmployees = db.query("SELECT E.initSecClearance FROM Employee E JOIN EmployeeLocation EL ON E.employeeID = EL.employeeID WHERE EL.locationID = %s", (employeeLocation,))

        # Check if all other employees in the same location have the same or higher security clearance
        return all(clearanceRanking[employee["initSecClearance"]] >= employeeSecLevel_value for employee in otherEmployees)

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e


def areInstalledAppsSafe(apps_on_phone):
    try:
        db = Database("SecurityRestrictions")

        # Iterate through the apps on the phone
        for app in apps_on_phone:
            package_name = app["packageName"]

            # Query the database to see if the package name is in the blacklist
            result = db.query("SELECT * FROM BlacklistedApps WHERE appID = %s", (package_name,))

            # If the result is not empty, the app is blacklisted, so the installed apps are not safe
            if result:
                return False

        # If none of the apps are blacklisted, the installed apps are safe
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e


    finally:
        db.con.close()


def isDeviceBrandUnsafe(brand):
    try:
        db = Database("SecurityRestrictions")
        # Query the database to see if the brand name is in the blacklist
        result = db.query("SELECT * FROM BlacklistedApps WHERE brandName = %s", (brand,))

        # If the result is not empty, the brand is blacklisted
        if result:
            return True

        # Otherwise, brand is not blacklisted
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e

def wasAppJustInstalled(firstInstallTime):
    try:
        # If first install time (in milliseconds) is less than 1 hour ago, the app was just installed, return True
        return firstInstallTime <= 3600000
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e





