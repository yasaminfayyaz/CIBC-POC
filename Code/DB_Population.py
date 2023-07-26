from DB_Operations import Database
from faker import Faker
import random
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
        vals = (dob, employeeID)
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

if __name__ == '__main__':
    db_employee = Database("Employees")
    employeeData(db_employee, 100)
    db_employee.con.close()


