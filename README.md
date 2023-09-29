# CIBC-POC
## Overview
This repository contains the codebase for a Zero Trust framework developed for CIBC. The framework leverages Attribute-Based Access Control (ABAC) to provide a robust and flexible access management solution.

## Components

### PEP
#### PEP/PEP_flask_app.py
The Policy Enforcement Point (PEP) serves as a critical component in a Zero Trust Architecture, designed to manage access requests and enforce security policies dynamically. It is built using Flask and integrates with a Policy Decision Point (PDP) through the pyxacml_sdk. The PEP acts as an intermediary that intercepts access requests, evaluates them based on various attributes, and communicates with the PDP to make an authorization decision.
##### Features
- React Native Zero Trust Agent Integration
- Dynamic Trust Attributes
- Trust Engine Interaction

#### PEP/pyxacml_sdk
The pyxacml_sdk directory contains a Python Client SDK for AuthzForce Server. This SDK was originally forked from [AuthzForce Community Edition](https://github.com/authzforce). Modifications were made to ensure compatibility with our Zero Trust framework implementation.

#### PEP/DB_Operations.py
The DB_Operations.py script serves as a communication bridge between the Policy Enforcement Point (PEP) and the Policy Information Point (PIP). It provides methods to interact with the MySQL-based PIP.

#### PEP/DB_Population.py
The DB_Population.py script is designed to populate the MySQL-based Policy Information Point (PIP) with mock data, particularly focusing on the employee and resource databases.

#### PEP/booleanChecks.py
The script offers a set of Boolean checks designed to dynamically evaluate employee attributes. Integrated with a Zero Trust agent, the methods in this code are called by the PEP to perform real-time assessments across various parameters such as location, device registration, work hours, and security clearance.

#### PEP/utils.py
Provides utility functions used by PEP to enhance the dynamic attributes. One function utilizes Wi-Fi fingerprinting to accurately determine an employee's indoor location, updating this information in the database. Another function converts string-based security labels into their numerical equivalents for easier data manipulation.

#### PEP/config.yaml
This file configures the Policy Decision Point (PDP) by specifying host, port, and endpoint details.

#### PEP/trustEngine.py
The Trust Engine is responsible for dynamically calculating an employee's trustworthiness based on various attributes. It employs a quadruple system to represent belief, disbelief, uncertainty, and base rate for each attribute. These quadruples are then used to compute a trust score through a fusion formula. The trust score is subsequently thresholded to determine the entity's clearance level.


### PAP
#### PAP/PAP.py
The PAP.py script serves as the Policy Administration Point (PAP) in the framework. Its primary role is to load XACML policies into the Policy Decision Point (PDP).

#### PAP/Digital Policy
Contains the ALFA policy, which has been auto-compiled into XACML format. This XACML policy must then be pushed to the PDP via the PAP.py.


### PIP Directory
The directory contains several key elements related to the MySQL Policy Information Point (PIP). It includes Data Definition Language scripts for database structure. There are also image files depicting the Entity-Relationship (ER) diagrams for various databases in addition to their current data.

---

## Hosting Information

### Policy Decision Point (PDP)
- Hosted on an Amazon EC2 instance running AuthzForce.
- Already configured and contains the policy.
- For manual setup and more about AuthzForce, refer to [AuthzForce Documentation](https://github.com/authzforce/server).

### Policy Enforcement Point (PEP)
- Hosted on PythonAnywhere.
- Requires all files from the `PEP` directory to be uploaded to the Flask application.
- For setup instructions, refer to [PythonAnywhere Documentation](https://help.pythonanywhere.com/pages/).

### Policy Information Point (PIP)
- Hosted on Amazon RDS (SQL).
- For manual setup, refer to [Amazon RDS Documentation](https://aws.amazon.com/rds/).

### Policy Administration Point (PAP)
- The PAP.py script can be run from any IDE.
- Must have access to the policy files for successful operation.


**Note:** URLs for accessing these components are provided separately. Sensitive information like passwords is securely shared in a separate file.

