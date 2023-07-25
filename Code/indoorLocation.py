from DB_Operations import Database
import numpy as np

def indoorLocation(BSSIDs, RSSIs):
    try:
        BSSID1, BSSID2, BSSID3 = BSSIDs
        AP1_RSSI_User = abs(RSSIs[0])
        AP2_RSSI_User = abs(RSSIs[1])
        AP3_RSSI_User = abs(RSSIs[2])

        db = Database("wifiReferenceInfo")
        locationIDs = [locationID["locationID"] for locationID in db.query("SELECT locationID FROM Location")]
        results = {}
        for locationID in locationIDs:
            RSSI_Ref1 = db.query("SELECT RSSI FROM Location_RSSI WHERE BSSID = %s AND locationID = %s", (BSSID1, locationID))
            RSSI_Ref2 = db.query("SELECT RSSI FROM Location_RSSI WHERE BSSID = %s AND locationID = %s", (BSSID2, locationID))
            RSSI_Ref3 = db.query("SELECT RSSI FROM Location_RSSI WHERE BSSID = %s AND locationID = %s", (BSSID3, locationID))
            if RSSI_Ref1 and RSSI_Ref2 and RSSI_Ref3:
                refPoint = np.array([int(RSSI_Ref1[0]["RSSI"]), int(RSSI_Ref2[0]["RSSI"]), int(RSSI_Ref3[0]["RSSI"])])
                livePoint = np.array((AP1_RSSI_User, AP2_RSSI_User, AP3_RSSI_User))
                dist = np.linalg.norm(livePoint - refPoint)
                results[locationID] = dist

        minDistID = min(results, key=results.get)
        getLocation = db.query("SELECT locationName FROM Location WHERE locationID = %s", (minDistID,))
        userLocation = getLocation[0]['locationName'] if getLocation else None
        return userLocation

    except Exception as e:
        print(f"An error occurred: {e}")
        return -1  # Return a custom error code

    finally:
        db.con.close()









if __name__ == '__main__':
    BSSIDs = ['34:FC:B9:7C:E3:80', 'E0:CB:BC:96:3D:0C', 'A8:5B:F7:29:7B:60']
    RSSIs = [-42, -83, -43]

    location = indoorLocation(BSSIDs, RSSIs)
    print(f"Location with original order of BSSIDs and RSSIs: {location}")


