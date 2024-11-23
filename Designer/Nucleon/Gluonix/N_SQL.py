from sqlite3 import connect as SQLite3_connect
from _thread import allocate_lock as Thread_allocate_lock, get_ident as Thread_get_ident

class SQL:
    def __init__(self, Database):
        self.Database = Database
        self.Local = {}
        self.Lock = Thread_allocate_lock()
        self.ReturnData = False
        self.Nothing = False

    def __str__(self):
        return "Sql[Database=" + str(self.Database) + "]"

    def __repr__(self):
        return "Sql[Database=" + str(self.Database) + "]"

    def GetConnection(self):
        ThreadId = Thread_get_ident()
        if ThreadId not in self.Local:
            Connection = SQLite3_connect(self.Database, uri=True, check_same_thread=False)
            Connection.execute("PRAGMA journal_mode=WAL")
            self.Local[ThreadId] = Connection
        return self.Local[ThreadId]

    def Get(self, Command, Keys=False):
        with self.Lock:
            Connection = self.GetConnection()
            Cursor = Connection.cursor()
            Rows = Cursor.execute(Command)
            Rows = Rows.fetchall()
            if Keys and "SELECT *" in Command.upper():
                Columns = Cursor.description
                Column = [Name[0] for Name in Columns]
                self.ReturnData = []
                for Row in Rows:
                    TempRow = {Column[X]: Row[X] for X in range(len(Column))}
                    self.ReturnData.append(TempRow)
            else:
                self.ReturnData = Rows
            return self.ReturnData

    def Post(self, Command, Keys=False):
        with self.Lock:
            Connection = self.GetConnection()
            Cursor = Connection.cursor()
            self.Nothing = Cursor.execute(Command)
            Connection.commit()

    def Close(self):
        ThreadId = Thread_get_ident()
        if ThreadId in self.Local:
            self.Local[ThreadId].close()
            del self.Local[ThreadId]