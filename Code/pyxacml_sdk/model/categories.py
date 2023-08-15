#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : model/categories.py
# Author            : hargathor <3949704+hargathor@users.noreply.github.com>
# Date              : 23.01.2018
# Last Modified Date: 23.01.2018
# Last Modified By  : hargathor <3949704+hargathor@users.noreply.github.com>

from enum import Enum
"""

"""


class Category_ID(Enum):
    subjectCat = "urn:oasis:names:tc:xacml:1.0:subject-category:access-subject"

    resourceCat = "urn:oasis:names:tc:xacml:3.0:attribute-category:resource"

    actionCat = "urn:oasis:names:tc:xacml:3.0:attribute-category:action"

    environmentCat = "urn:oasis:names:tc:xacml:3.0:attribute-category:environment"


def __str__(self):
        return '{0}'.format(self.value)
