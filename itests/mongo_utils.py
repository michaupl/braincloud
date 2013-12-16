# coding: utf-8
from django.test.runner import DiscoverRunner

from mongoengine import connect
from mongoengine.connection import disconnect

from brainblog.index import delete_index


class MongoTestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        # set up sqlite
        old_config = super(MongoTestRunner, self).setup_databases(**kwargs)
        # set up mongo
        db_name = 'braincloud_test'
        disconnect()
        connect(db_name)
        print 'Creating test database: ' + db_name
        delete_index('_all')
        print 'Deleting all indexes.'
        return {'sqlite': old_config, 'mongo': db_name}

    def teardown_databases(self, old_config, **kwargs):
        db_name = old_config['mongo']
        old_sqlite_config = old_config['sqlite']
        super(MongoTestRunner, self).teardown_databases(old_sqlite_config, **kwargs)
        from pymongo import Connection
        conn = Connection()
        conn.drop_database(db_name)
        print 'Dropping test database: ' + db_name
        delete_index('_all')
        print 'Deleting all indexes.'