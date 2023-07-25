CREATE TABLE Employee (
    employeeID CHAR(10) PRIMARY KEY,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    jobRole VARCHAR(255) NOT NULL,
    initSecClearance ENUM('Top Secret', 'Secret', 'Confidential', 'Unclassified') NOT NULL,
    primaryBranch VARCHAR(255) NOT NULL,
    DateOfBirth DATE NOT NULL
);
CREATE TABLE Password (
    PasswordID INT PRIMARY KEY,
    PasswordHash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    employeeID CHAR(10) NOT NULL,
    FOREIGN KEY (employeeID) REFERENCES Employee(employeeID) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE Device (
    deviceID INT PRIMARY KEY,
    employeeID CHAR(10) NOT NULL,
    FOREIGN KEY (employeeID) REFERENCES Employee(employeeID) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE Resource (
    resourceID INT PRIMARY KEY,
    resourceType VARCHAR(255) NOT NULL,
    secLevel ENUM('Top Secret', 'Secret', 'Confidential', 'Unclassified') NOT NULL
);
CREATE TABLE AP (
    SSID VARCHAR(255) NOT NULL,
    BSSID VARCHAR(255) PRIMARY KEY,
    accessPointNum ENUM('1', '2', '3') NOT NULL
);


CREATE TABLE Location (
    locationID INT PRIMARY KEY,
    clusterID ENUM('1', '2', '3') NOT NULL,
    locationName VARCHAR(255) NOT NULL,
    isTrusted ENUM('0', '1') NOT NULL
);

CREATE TABLE Location_RSSI (
    measurementID INT PRIMARY KEY,
    locationID INT NOT NULL,
    BSSID VARCHAR(255) NOT NULL,
    RSSI INT NOT NULL,
    FOREIGN KEY (locationID) REFERENCES Location(locationID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (BSSID) REFERENCES AP(BSSID) ON DELETE CASCADE ON UPDATE CASCADE
);
