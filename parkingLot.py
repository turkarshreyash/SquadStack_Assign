import sqlite3

class Parking:

    def initTable(self, pSlots) -> bool:
        dbCurr = self.dbConn.cursor()
        createTableCommand = """CREATE TABLE slots (sNumber INTEGER PRIMARY KEY, rNumber VARCHAR(13), dAge INTEGER, sStatus VARCHAR (5));"""
        dbCurr.execute(createTableCommand)
        for i in range(1, pSlots+1):
            insertSlotCommand = """INSERT INTO slots VALUES ("""+str(
                i)+""","", 0, "FREE");"""
            dbCurr.execute(insertSlotCommand)

        self.dbConn.commit()
        return True

    def __init__(self, pSlots: int, dbFile: str):
        self.pSlots = pSlots
        self.dbFile = dbFile
        self.dbConn = sqlite3.connect(dbFile)
        self.initTable(pSlots)

    def arrive(self, rNumber: str, dAge: int) -> int:
        dbCurr = self.dbConn.cursor()
        getMinCommand = """SELECT min(snumber) from slots where sStatus = "FREE";"""
        dbCurr.execute(getMinCommand)
        min_sNumber = dbCurr.fetchone()[0]
        if min_sNumber == None:
            return -1
        #print(min_sNumber)
        updateQuery = """UPDATE slots SET rnumber='"""+rNumber+"""', dAge =""" + \
            str(dAge)+""", sStatus = "OCC" where snumber=""" + \
            str(min_sNumber)+""";"""
        #print(updateQuery)
        dbCurr.execute(updateQuery)
        self.dbConn.commit()
        return min_sNumber

    def depart(self, sNumber: int) -> ():
        dbCurr = self.dbConn.cursor()
        getSlotCommand = """SELECT * from slots where sStatus = "OCC" and snumber=""" + \
            str(sNumber)+""";"""
        dbCurr.execute(getSlotCommand)
        slot = dbCurr.fetchone()
        if slot == None:
            return []
        updateQuery = """UPDATE slots SET rnumber="", dAge = 0, sStatus = "FREE" where snumber=""" + \
            str(sNumber)+""";"""
        #print(updateQuery)
        dbCurr.execute(updateQuery)
        return list(slot)

    def getSlots_withDAge(self, dAge: int) -> list:
        dbCurr = self.dbConn.cursor()
        query = """SELECT snumber from slots where dAge="""+str(dAge)+""";"""
        dbCurr.execute(query)
        result = dbCurr.fetchall()
        if result == []:
            return []
        sNumber = [i[0] for i in result]
        #print(sNumber)
        return sNumber

    def getSlot_withRNumber(self, rNumber: str) -> int:
        dbCurr = self.dbConn.cursor()
        query = """SELECT sNumber from slots where rNumber='""" + \
            str(rNumber)+"""';"""
        dbCurr.execute(query)
        result = dbCurr.fetchone()
        if result == None:
            return -1
        #print(result)
        return result[0]

    def getRNumber_withDAge(self, dAge: int) -> list:
        dbCurr = self.dbConn.cursor()
        query = """SELECT rnumber from slots where dage="""+str(dAge)+""";"""
        dbCurr.execute(query)
        result = dbCurr.fetchall()
        if result == []:
            return []
        rNumber = [i[0] for i in result]
        #print(rNumber)
        return rNumber
