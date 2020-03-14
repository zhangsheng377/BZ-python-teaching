# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .database_pymongo import DataBasePyMongo


def DataBaseFactory(database_name, sheet_name, model="pymongo"):
    if model == "pymongo":
        return DataBasePyMongo(database_name=database_name, sheet_name=sheet_name)
    else:
        raise ValueError('model name: {} can not find.'.format(model))
        pass
    return None
