from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Instance, Document, fields, Schema, ValidationError
import asyncio
from bson.objectid import ObjectId
import pymongo
import datetime
import pytz
from collections import OrderedDict
import os
import data
from pprint import pprint


db = AsyncIOMotorClient(data.DB_HOST, port=data.DB_PORT)[data.DB_NAME]
instance = Instance(db)


@instance.register
class User(Document):
    class Meta:
        collection_name = 'users'
        indexes = []

    id = fields.IntField(required=True, unique=True, attribute='_id')
    process_flag = fields.BooleanField(default=False)
    created = fields.DateTimeField(required=True)
    visited = fields.DateTimeField(required=True)
    username = fields.StrField(required=True, allow_none=True)
    first_name = fields.StrField(required=True)
    last_name = fields.StrField(required=True, allow_none=True, default=None)
    language_code = fields.StrField(required=True, allow_none=True)
    language = fields.StrField(required=True)


async def create_indexes():
    await User.ensure_indexes()


if __name__ == '__main__':
    pass
