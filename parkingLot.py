import sqlite3



class Parking:

    #creates db table
    def initTable(self, pSlots) -> bool:
        dbCurr = self.dbConn.cursor()
        createTableCommand = """CREATE TABLE slots (sNumber INTEGER PRIMARY KEY, rNumber VARCHAR(13), dAge INTEGER, sStatus VARCHAR (5));"""
        dbCurr.execute(createTableCommand)

        #inserts pSlots(arg given by testcase)
        for i in range(1, pSlots+1):
            insertSlotCommand = """INSERT INTO slots VALUES ("""+str(
                i)+""","", 0, "FREE");"""
            dbCurr.execute(insertSlotCommand)

        self.dbConn.commit()
        return True

    #constructor
    #create a connection and call function to create table
    def __init__(self, pSlots: int, dbFile: str):
        self.pSlots = pSlots
        self.dbFile = dbFile
        self.dbConn = sqlite3.connect(dbFile)
        self.initTable(pSlots)


    #handles park query
    def arrive(self, rNumber: str, dAge: int) -> int:
        dbCurr = self.dbConn.cursor()

        #find slot with mini slot number
        getMinCommand = """SELECT min(snumber) from slots where sStatus = "FREE";"""
        dbCurr.execute(getMinCommand)
        min_sNumber = dbCurr.fetchone()[0]

        #parking full
        if min_sNumber == None:
            return -1

        #update slot to OCC (occupied) with vechicle registeration umber and driver age.
        #print(min_sNumber)
        updateQuery = """UPDATE slots SET rnumber='"""+rNumber+"""', dAge =""" + \
            str(dAge)+""", sStatus = "OCC" where snumber=""" + \
            str(min_sNumber)+""";"""
        #print(updateQuery)

        dbCurr.execute(updateQuery)
        self.dbConn.commit()

        #return slot number
        return min_sNumber

    #handles query for vechicle departure
    def depart(self, sNumber: int) -> ():
        dbCurr = self.dbConn.cursor()

        #get registeration number and driver age
        getSlotCommand = """SELECT * from slots where sStatus = "OCC" and snumber=""" + \
            str(sNumber)+""";"""
        dbCurr.execute(getSlotCommand)
        slot = dbCurr.fetchone()
        if slot == None:
            return []

        #update slot to FREE
        updateQuery = """UPDATE slots SET rnumber="", dAge = 0, sStatus = "FREE" where snumber=""" + \
            str(sNumber)+""";"""
        #print(updateQuery)
        dbCurr.execute(updateQuery)
        
        #return details (registeration number and driver age)
        return list(slot)

    #handle get slot with driver age query
    def getSlots_withDAge(self, dAge: int) -> list:
        dbCurr = self.dbConn.cursor()

        #find in db 
        query = """SELECT snumber from slots where dAge="""+str(dAge)+""";"""
        dbCurr.execute(query)
        result = dbCurr.fetchall()
        #handle no result
        if result == []:
            return []
        sNumber = [i[0] for i in result]
        #print(sNumber)
        #return list wiht slot numbers
        return sNumber

    #handle get slot with vechile registeration number
    def getSlot_withRNumber(self, rNumber: str) -> int:
        dbCurr = self.dbConn.cursor()
        #find slot with vechilce registeration number 
        query = """SELECT sNumber from slots where rNumber='""" + \
            str(rNumber)+"""';"""
        dbCurr.execute(query)
        result = dbCurr.fetchone()
        #handle no result
        if result == None:
            return -1
        #print(result)
        return result[0]

    #handle get vechile registeartion number wiht driver age
    def getRNumber_withDAge(self, dAge: int) -> list:
        dbCurr = self.dbConn.cursor()
        #select query to get slot
        query = """SELECT rnumber from slots where dage="""+str(dAge)+""";"""
        dbCurr.execute(query)
        result = dbCurr.fetchall()
        #handle no result
        if result == []:
            return []
        rNumber = [i[0] for i in result]
        #print(rNumber)
        #return registeration numbers
        return rNumber
