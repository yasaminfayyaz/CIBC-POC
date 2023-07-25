from geopy.distance import geodesic
from DB_Operations import Database
from datetime import datetime

def isAtPrimaryBranch(employeeID, currentLat, currentLong):
    try:
        db = Database("Employees")
        radius = 0.1
        primaryBranchID = db.query("SELECT primaryBranchID FROM Employee WHERE employeeID = %s", (employeeID,))[0]['primaryBranchID']
        branchLocation = db.query("SELECT latitude, longitude FROM Branch WHERE branchID = %s", (primaryBranchID,))[0]
        branchLat = branchLocation['latitude']
        branchLong = branchLocation['longitude']
        # Calculate the distance between the current location and the branch location
        distance = geodesic((currentLat, currentLong), (branchLat, branchLong)).kilometers
        # Compare the distance with the radius
        return distance <= radius
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        db.con.close()

def isRegisteredDevice(employeeID, currentDeviceID):
    try:
        db = Database("Employees")
        registeredDeviceID = db.query("SELECT deviceID FROM Device WHERE employeeID = %s", (employeeID,))
        if registeredDeviceID:
            return registeredDeviceID[0]['deviceID'] == currentDeviceID
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        db.con.close()


def isWorkHours():
    now = datetime.now()

    # Check if today is a weekday (0 = Monday, 6 = Sunday)
    if now.weekday() >= 5:  # If it's Saturday or Sunday
        return False

    # Define work hours start and end
    work_Hours_Start = now.replace(hour=8, minute=0, second=0, microsecond=0)
    work_Hours_End = now.replace(hour=18, minute=0, second=0, microsecond=0)


    if work_Hours_Start <= now <= work_Hours_End:
        return True
    else:
        return False

if __name__ == '__main__':

    print(f"Employee is currently at primary branch: {isAtPrimaryBranch(100000000, 43.9478, -78.8991)}")
    print(f"Employee is accessing resource during work hours: {isWorkHours()}")


