from DB_Operations import Database
import numpy as np

def indoorLocation(BSSIDs, RSSIs, employeeID):
    """
     This function uses the Wi-Fi fingerprinting technique where the signal strengths associated with
     multiple access points are stored as fingerprints for different indoor locations. The current RSSI readings
     from the user's phone are then compared with these fingerprints to determine the most probable location.

     Parameters:
     - BSSIDs (list): A list of MAC addresses of Wi-Fi access points.
     - RSSIs (list): A list of RSSIs corresponding to the access points.
     - employeeID (str/int): The unique identifier for the employee.

     Returns:
     - str: The name of the location where the employee is currently located.

     Process:
     1. Extracts the MAC addresses of the access points and corresponding RSSIs.
     2. Connects to the "LocationReference" database to fetch reference RSSIs for known indoor locations.
     3. Calculates the Euclidean distance between the live RSSI readings and the reference RSSIs for each location.
     4. Determines the location with the minimum distance as the most probable current location of the employee.
     5. Updates the "Employees" database with the determined location for the given employeeID.
     6. Returns the name of the determined location.

     """
    try:
        BSSID1, BSSID2, BSSID3 = BSSIDs
        AP1_RSSI_User = abs(RSSIs[0])
        AP2_RSSI_User = abs(RSSIs[1])
        AP3_RSSI_User = abs(RSSIs[2])

        db_location = Database("LocationReference")
        locationIDs = [locationID["locationID"] for locationID in db_location.query("SELECT locationID FROM Location")]
        results = {}
        for locationID in locationIDs:
            RSSI_Ref1 = db_location.query("SELECT RSSI FROM Location_RSSI WHERE BSSID = %s AND locationID = %s", (BSSID1, locationID))
            RSSI_Ref2 = db_location.query("SELECT RSSI FROM Location_RSSI WHERE BSSID = %s AND locationID = %s", (BSSID2, locationID))
            RSSI_Ref3 = db_location.query("SELECT RSSI FROM Location_RSSI WHERE BSSID = %s AND locationID = %s", (BSSID3, locationID))
            if RSSI_Ref1 and RSSI_Ref2 and RSSI_Ref3:
                refPoint = np.array([int(RSSI_Ref1[0]["RSSI"]), int(RSSI_Ref2[0]["RSSI"]), int(RSSI_Ref3[0]["RSSI"])])
                livePoint = np.array((AP1_RSSI_User, AP2_RSSI_User, AP3_RSSI_User))
                dist = np.linalg.norm(livePoint - refPoint)
                results[locationID] = dist

        minDistID = min(results, key=results.get)


        getLocation = db_location.query("SELECT locationName FROM Location WHERE locationID = %s", (minDistID,))

        #add locationID of user's location to DB
        db_employee = Database("Employees")
        db_employee.insert("INSERT INTO EmployeeLocation (employeeID, locationID) VALUES (%s, %s) ON DUPLICATE KEY UPDATE locationID = %s", (employeeID, minDistID, minDistID))

        userLocation = getLocation[0]['locationName'] if getLocation else None
        return userLocation

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        db_location.con.close()
        db_employee.con.close()

def stringSecLabel_to_int(label):
    """
       Converts a security label string to its corresponding integer value.

       Parameters:
       - label (str): The security label as a string.

       Returns:
       - int: The integer value corresponding to the security label.

       """
    mapping = {"Top Secret" : 5, "Secret" : 4, "Confidential" : 3, "Restricted" : 2, "Unclassified" : 1}
    return mapping[label]


def get_base_rate(employeeID, attribute_id):
    """
        Retrieves the base rate of a specific attribute for a given employee.

        Parameters:
        - employeeID (str/int): The unique identifier for the employee.
        - attribute_id (str): The ID of the attribute for which the base rate is to be fetched.

        Returns:
        - float: The base rate of the specified attribute for the given employee.

        """
    db = Database("Employees")
    base_rate_query = f"SELECT {attribute_id} FROM TrustAttributes WHERE employeeID = %s"
    result = db.query(base_rate_query, (employeeID,))[0][attribute_id]
    db.con.close()
    return result


def update_base_rate(employeeID, attribute_id, new_value):
    """
       Updates the base rate of a specific attribute for a given employee.

       Parameters:
       - employeeID (str/int): The unique identifier for the employee.
       - attribute_id (str): The ID of the attribute for which the base rate is to be updated.
       - new_value (bool): The new value (True/False) to be considered for updating the base rate.

       Process:
       1. Converts the boolean new_value to its corresponding numerical value.
       2. Fetches the current base rate for the specified attribute.
       3. Calculates the average of the current base rate and the new numerical value.
       4. Updates the base rate in the database with the calculated average.
       5. Closes the database connection.
       """
    # Convert boolean values to numerical values
    new_value_numerical = 1 if new_value else 0

    db = Database("Employees")
    # Fetch the current base rate
    current_base_rate_query = f"SELECT {attribute_id} FROM TrustAttributes WHERE employeeID = %s"
    current_base_rate = db.query(current_base_rate_query, (employeeID,))[0][attribute_id]

    # Calculate the average of the current base rate and the new numerical value
    updated_base_rate = (current_base_rate + new_value_numerical) / 2

    # Update the base rate in the database
    update_base_rate_query = f"UPDATE TrustAttributes SET {attribute_id} = %s WHERE employeeID = %s"
    db.update(update_base_rate_query, (updated_base_rate, employeeID))

    # Close the database connection
    db.con.close()

