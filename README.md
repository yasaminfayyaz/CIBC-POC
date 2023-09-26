# CIBC-POC
Overview
This repository contains the codebase for a Zero Trust framework developed for CIBC. The framework leverages Attribute-Based Access Control (ABAC) to provide a robust and flexible access management solution.


Components
Code/PEP_flask_app.py
The Policy Enforcement Point (PEP) serves as a critical component in a Zero Trust Architecture, designed to manage access requests and enforce security policies dynamically. It is built using Flask and integrates with a Policy Decision Point (PDP) through the pyxacml_sdk. The PEP acts as an intermediary that intercepts access requests, evaluates them based on various attributes, and communicates with the PDP to make an authorization decision.
    Features
    React Native Zero Trust Agent Integration
    The PEP is designed to work seamlessly with a React Native Zero Trust agent. The agent communicates with the PEP to send access requests and other necessary operational data.
    
    Dynamic Trust Attributes
    The PEP calculates dynamic trust attributes such as the safety of installed apps, location trustworthiness, and work hours. These attributes are then sent to the PDP for an authorization   
    decision.

    Trust Engine Interaction
    Syncs with the Trust Engine to update security clearances dynamically.

Code/pyxacml_sdk
The pyxacml_sdk directory contains a Python Client SDK for AuthzForce Server. This SDK was originally forked from AuthzForce Community Edition https://github.com/authzforce. Modifications were made to ensure compatibility with our Zero Trust framework implementation.

Code/DB_Operations.py
The DB_Operations.py script serves as a communication bridge between the Policy Enforcement Point (PEP) and the Policy Information Point (PIP). It provides methods to interact with the MySQL-based PIP.

Code/DB_Population.py
The DB_Population.py script is designed to populate the MySQL-based Policy Information Point (PIP) with mock data, particularly focusing on the employee and resource databases.

Code/booleanChecks.py
The script offers a set of Boolean checks designed to dynamically evaluate employee attributes. Integrated with a Zero Trust agent, the methods in this code are called by the PEP to perform real-time assessments across various parameters such as location, device registration, work hours, and security clearance. Using custom database queries, geodesic calculations, etc, it generates new trust attributes essential for making informed and secure access decisions.

Code/utils.py
Provides utility functions used by PEP to enhance the dynamic attributes  One function utilizes Wi-Fi fingerprinting to accurately determine an employee's indoor location, updating this information in the database. Another function converts string-based security labels into their numerical equivalents for easier data manipulation. The code also includes functions for retrieving and updating the base rate of specific trust attributes for an employee, interacting directly with the database to do so.

Code/PAP.py
The PAP.py script serves as the Policy Administration Point (PAP) in the framework. Its primary role is to load XACML policies into the Policy Decision Point (PDP). This ensures that the PDP has the necessary policy information for making access control decisions.



