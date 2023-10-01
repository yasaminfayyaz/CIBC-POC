#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : model/attribute_ids.py
# Author            : hargathor <3949704+hargathor@users.noreply.github.com>
# Date              : 24.01.2018
# Last Modified Date: 24.01.2018
# Last Modified By  : hargathor <3949704+hargathor@users.noreply.github.com>

from enum import Enum


class Attribute_ID(Enum):
    SUBJECT_ID = "urn:oasis:names:tc:xacml:1.0:subject:subject-id"
    SUBJECT_ID_QUALIFIER = "urn:oasis:names:tc:xacml:1.0:subject:subject-id-qualifier"
    KEY_INFO = "urn:oasis:names:tc:xacml:1.0:subject:key-info"
    AUTHENTICATION_TIME = "urn:oasis:names:tc:xacml:1.0:subject:authentication-time"
    AUTHENTICATION_METHOD = "urn:oasis:names:tc:xacml:1.0:subject:authentication-method"
    REQUEST_TIME = "urn:oasis:names:tc:xacml:1.0:subject:request-time"
    SESSION_START = "urn:oasis:names:tc:xacml:1.0:subject:session-start-time"
    AUTHN_LOCALITY_IP_ADDRESS = "urn:oasis:names:tc:xacml:3.0:subject:authn-locality:ip-address"
    AUTHN_LOCALITY_DNS_NAME = "urn:oasis:names:tc:xacml:3.0:subject:authn-locality:dns-name"
    RESOURCE_ID = "urn:oasis:names:tc:xacml:1.0:resource:resource-id"
    TARGET_NAMESPACE = "urn:oasis:names:tc:xacml:2.0:resource:target-namespace"
    ACTION_ID = "urn:oasis:names:tc:xacml:1.0:action:action-id"
    IMPLIED_ACTION = "urn:oasis:names:tc:xacml:1.0:action:implied-action"
    CURRENT_TIME = "urn:oasis:names:tc:xacml:1.0:environment:current-time"
    CURRENT_DATE = "urn:oasis:names:tc:xacml:1.0:environment:current-date"
    CURRENT_DATEXML = "urn:oasis:names:tc:xacml:1.0:environment:current-http://www.w3.org/2001/XMLSchema#date"

    #Custom attributes defined by us

    INSTALLED_APPS_SAFE = "urn:custom:device:installed-apps-safe"
    LOCATION_TRUSTED = "urn:custom:device:location:location-trusted"
    DEVICE_REGISTERED = "urn:custom:device:device-registered"
    DEVICE_REDFLAGS = "urn:custom:device:redflags"
    WORK_HOURS = "urn:custom:environment:work-hours"
    SUFFICIENT_CLEARANCE = "urn:custom:employee:sufficient-clearance"
    SUFFICIENT_CLEARANCE_EXISTS = "urn:custom:employee:sufficient-clearance-exists"
    AT_PRIMARY_BRANCH = "urn:custom:employee:at-primary-branch"

    EMPLOYEE_DEPARTMENT = "urn:custom:employee:department"
    EMPLOYEE_INIT_CLEARANCE = "urn:custom:employee:initial-clearance"
    EMPLOYEE_CURRENT_CLEARANCE = "urn:custom:employee:current-clearance"


    RESOURCE_DEPARTMENT = "urn:custom:resource:department"
    RESOURCE_TYPE = "urn:custom:resource:type"
    RESOURCE_SEC_LEVEL = "urn:custom:resource:security-level"


    def __str__(self):
        return '{0}'.format(self.value)
