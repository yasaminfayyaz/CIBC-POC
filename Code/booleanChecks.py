from geopy.distance import geodesic
from DB_Operations import Database
from datetime import datetime

def isAtPrimaryBranch(employeeID, currentLat, currentLong):
    """
       Determines if an employee is at their primary branch.

       Parameters:
       - employeeID: The unique identifier for the employee.
       - currentLat: The current latitude of the employee.
       - currentLong: The current longitude of the employee.

       Returns:
       - True if the employee is at their primary branch, False otherwise.

       Process:
       - Queries the database to get the primary branch location for the given employee.
       - Calculates the distance between the current location and the primary branch location.
       - If the distance is within a specified radius, the function returns True, otherwise False.
       """
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
    """
    Determines if an employee is at a trusted indoor location.

    Parameters:
    - employeeID: The unique identifier for the employee.

    Returns:
    - True if the employee is at a trusted indoor location, False otherwise.

    Process:
    - Queries the database to fetch the location ID associated with the employee.
    - Checks if the location is marked as trusted in the reference database.
    """

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
    """
        Checks if the current device is registered to the employee.

        Parameters:
        - employeeID: The unique identifier for the employee.
        - currentDeviceID: The unique ID of the device currently being used.

        Returns:
        - True if the device is registered to the employee, False otherwise.

        Process:
        - Queries the database to get the registered device ID for the given employee.
        - Compares the registered device ID with the current device ID.
        """
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
    """
       Determines if the current time falls within work hours.

       Parameters:
       - None

       Returns:
       - True if the current time is within work hours, False otherwise.

       Process:
       - Checks the current day of the week.
       - Defines the start and end of work hours.
       - Compares the current time with the defined work hours.
       """
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
    """
       Determines if all employees in the same indoor location as the current employee have the same or higher security clearance.

       Parameters:
       - employeeID: The unique identifier for the employee.

       Returns:
       - True if all employees in the same location have the same or higher security clearance as the current employee, False otherwise.

       Process:
       - Queries the database to get the security clearance of the given employee.
       - Fetches the location of the given employee.
       - Retrieves the security clearances of all other employees in the same location.
       - Compares the security clearance of each employee in the location with the current employee's clearance.
       """
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
    """
        Determines if the apps installed on a phone are safe.

        Parameters:
        - apps_on_phone: List of apps installed on the phone.

        Returns:
        - True if all apps are safe, False if any app is blacklisted.

        Process:
        - Iterates through the apps on the phone.
        - Queries the database to check if any app is blacklisted.
        """
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
    """
        Checks if a device brand is considered unsafe.

        Parameters:
        - brand: The brand name of the device.

        Returns:
        - True if the brand is blacklisted, False otherwise.

        Process:
        - Queries the database to check if the brand name is blacklisted.
        """
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
    """
        Determines if an app was recently installed.

        Parameters:
        - firstInstallTime: The installation time of the app in milliseconds.

        Returns:
        - True if the app was installed within the last hour, False otherwise.

        Process:
        - Compares the first installation time with the current time.
        """
    try:
        # If first install time (in milliseconds) is less than 1 hour ago, the app was just installed, return True
        return firstInstallTime <= 3600000
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e





