from sqlite3 import connect
from threading import Lock, get_ident

class SQL():
    
    def __init__(self, Path):
        self._Path = Path
        self._Local = {}
        self._Lock = Lock()
        self._ReturnData = False
        self._Nothing = False

    def __str__(self):
        return f"SQL[Database:{self._Path}]"

    def __repr__(self):
        return f"SQL[Database:{self._Path}]"

    def __dir__(self):
        return []

    @property
    def __dict__(self):
        return {}

    def GetConnection(self):
        ThreadId = get_ident()
        if ThreadId not in self._Local:
            Connection = connect(self._Path, uri=True, check_same_thread=False)
            Connection.execute("PRAGMA journal_mode=WAL")
            self._Local[ThreadId] = Connection
        return self._Local[ThreadId]

    def Get(self, Command, Keys=True):
        with self._Lock:
            Connection = self.GetConnection()
            Cursor = Connection.cursor()
            Rows = Cursor.execute(Command)
            Rows = Rows.fetchall()
            if Keys and "SELECT *" in Command.upper():
                Columns = Cursor.description
                Column = [Name[0] for Name in Columns]
                self._ReturnData = []
                for Row in Rows:
                    TempRow = {Column[X]: Row[X] for X in range(len(Column))}
                    self._ReturnData.append(TempRow)
            else:
                self._ReturnData = Rows
            return self._ReturnData

    def Post(self, Command, Keys=False):
        with self._Lock:
            Connection = self.GetConnection()
            Cursor = Connection.cursor()
            self._Nothing = Cursor.execute(Command)
            Connection.commit()

    def Close(self):
        ThreadId = get_ident()
        if ThreadId in self._Local:
            self._Local[ThreadId].close()
            del self._Local[ThreadId]