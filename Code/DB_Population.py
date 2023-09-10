from DB_Operations import Database
from faker import Faker
import random
import bcrypt
from datetime import date
fake = Faker()


departments = ["Customer Service", "Accounting", "Risk Management", "Loan Processing", "Mortgage Services",
                        "Investment Banking", "Compliance", "Human Resources", "Information Technology", "Marketing"]

securityLabels = ["Top Secret", "Secret", "Confidential", "Restricted", "Unclassified"]

def employeeData(db, numEmployees):
    branches = [100, 101, 102]
    startDate = date(1960, 1, 1)
    endDate = date(2005, 1, 1)
    id = 100000000
    for i in range(numEmployees):
        employeeID = id
        firstName = fake.first_name()
        lastName = fake.last_name()
        department = random.choice(departments)
        secClearance = random.choice(securityLabels)
        primaryBranchID= random.choice(branches)
        dob = fake.date_between(start_date = startDate, end_date = endDate)
        query = "Insert INTO Employee (employeeID, firstName, lastName, department, initSecClearance, primaryBranchID, DateOfBirth) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"
        vals = (employeeID, firstName, lastName, department, secClearance, primaryBranchID, dob)
        db.insert(query, vals)
        id = id + 1
        query = "Insert INTO Password (passwordHash, employeeID) \
                                VALUES (%s, %s)"
        salt = bcrypt.gensalt()
        dob = dob.strftime("%Y-%m-%d")
        defaultPass =  bcrypt.hashpw(dob.encode('utf-8'), salt)

        vals = (defaultPass, employeeID)
        db.insert(query, vals)


def resourceData(db, numResources):
    resourceTypes = ["Records", "Archives", "Documents", "Artifacts", "Information Assets", "Intellectual Property", "Research Materials"]
    id = 100000000
    for i in range(numResources):
        resourceID = id
        resourceName = fake.file_name()
        department = random.choice(departments)
        resourceType = random.choice(resourceTypes)
        secLevel = random.choice(securityLabels)
        query = "INSERT INTO Resource (resourceID, resourceName, department, resourceType, secLevel) \
                        VALUES (%s, %s, %s, %s, %s)"
        vals = (resourceID, resourceName, department, resourceType, secLevel)
        db.insert(query, vals)
        id = id + 1

def trustAttributes(db):
    # Get all employee IDs and their clearance levels
    employees = db.query("SELECT employeeID, initSecClearance FROM Employee")

    # Iterate through employees and set default values based on clearance level
    for employee in employees:
        clearance = employee["initSecClearance"]
        default_value = 0.5  # Default for "Unclassified"

        if clearance == "Top Secret":
            default_value = 0.9
        elif clearance == "Secret":
            default_value = 0.8
        elif clearance == "Confidential":
            default_value = 0.7
        elif clearance == "Restricted":
            default_value = 0.6

        # Create an SQL query to insert the attributes into the TrustAttributes table
        query = """
        INSERT INTO TrustAttributes (
            employeeID,
            INSTALLED_APPS_SAFE,
            AT_PRIMARY_BRANCH,
            LOCATION_TRUSTED,
            DEVICE_REGISTERED,
            WORK_HOURS,
            SUFFICIENT_CLEARANCE,
            NOT_EMULATOR,
            LOCATION_NOT_MOCKED,
            BRAND_SAFE,
            APP_NOT_JUST_INSTALLED,
            PIN_OR_FINGERPRINT_SET
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (employee["employeeID"], default_value, default_value, default_value, default_value, default_value, default_value, default_value, default_value, default_value, default_value, default_value)

        # Insert the attributes into the TrustAttributes table
        db.insert(query, values)


if __name__ == '__main__':
    db_employee = Database("Employees")
    trustAttributes(db_employee)
    db_employee.con.close()


