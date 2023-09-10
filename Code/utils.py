from DB_Operations import Database
import numpy as np

def indoorLocation(BSSIDs, RSSIs, employeeID):
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
    mapping = {"Top Secret" : 5, "Secret" : 4, "Confidential" : 3, "Restricted" : 2, "Unclassified" : 1}
    return mapping[label]


def get_base_rate(employeeID, attribute_id):
    db = Database("Employees")
    base_rate_query = f"SELECT {attribute_id} FROM TrustAttributes WHERE employeeID = %s"
    result = db.query(base_rate_query, (employeeID,))[0][attribute_id]
    db.con.close()
    return result


def update_base_rate(employeeID, attribute_id, new_value):
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
    db.insert(update_base_rate_query, (updated_base_rate, employeeID))

    # Close the database connection
    db.con.close()
