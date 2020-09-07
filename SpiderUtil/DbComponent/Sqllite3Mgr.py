import sqlite3
from Decorator.Singleton import singleton

class Sqllite3Connection(object):
    def __init__(self, db):
        self.filename = db
        self.connection = sqlite3.connect(db)

    def __del__(self):
        if self.connection:
            self.connection.close()

    def Query(self, sql):
        data = self.connection.execute(sql)
        return data
    

    def Execute(self, sql):
        self.connection.execute(sql)
        self.connection.commit()

    
    def Close(self):
        if self.connection:
            self.connection.close()
            self.connection = None


@singleton
class Sqlliet3Mgr(object):
    def __init__(self):
        self.DBMap = dict()

    
    def __del__(self):
        for db in self.DBMap:
            self.DBMap[db].Close()

    def GenerateDB(self, db):
        if self.DBMap.get(db, None) is None:
            self.DBMap[db] = Sqllite3Connection(db)

    
    def GetDB(self, db)->Sqllite3Connection:
        return self.DBMap.get(db, None)


g_sqllite_mgr = Sqlliet3Mgr()