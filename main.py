import parkingLot
import datetime
import os
import sys


def red(s: str): print("\x1b[31;1m", s, "\x1b[0m")
def green(s: str): print("\x1b[32;1m", s, "\x1b[0m")
def blue(s: str): print("\x1b[33;1m", s, "\x1b[0m")
def yellow(s: str): print("\x1b[36;1m", s, "\x1b[0m")


argc = len(sys.argv)
if(argc < 2):
    red("No TestCase file Provided!")
    exit()

testCaseFile = sys.argv[1]
dbFile = "DB_"+str(datetime.datetime.now()).replace(" ", "_") + ".sqlite3"

testCase = open(testCaseFile)

parking = None

for t in testCase:
    tokens = t.split()
    #print(tokens)
    if(tokens[0] == "Create_parking_lot"):
        parking = parkingLot.Parking(int(tokens[1]), dbFile)
        blue("Created parking of "+str(tokens[1])+" slots")

    if(tokens[0] == "Park"):
        rNumber = tokens[1]
        dAge = int(tokens[3])
        sNumber = parking.arrive(rNumber, dAge)
        if sNumber == -1:
            red("Parking Full")
        else:
            green(str("Car with vehicle registration number" +
                      str(rNumber)+" has been parked at slot number: "+str(sNumber)))

    if(tokens[0] == "Slot_numbers_for_driver_of_age"):
        dAge = int(tokens[1])
        result = parking.getSlots_withDAge(dAge)
        if result == []:red("null")
        else:blue(str(result))

    if(tokens[0] == "Slot_number_for_car_with_number"):
        rNumber = tokens[1]
        result = parking.getSlot_withRNumber(rNumber)
        if result == -1:red("No car found")
        else:blue(result)

    if(tokens[0] == "Leave"):
        sNumber = tokens[1]
        result = parking.depart(sNumber)
        if result == []:red(str("No car was parked at "+sNumber))
        else:
            yellow(str("Slot number "+sNumber+" vacated, the car with vehicle registration number "+result[1]+" left the space, the driver of the car was of age "+str(result[2])))

    if(tokens[0] == "Vehicle_registration_number_for_driver_of_age"):
        dAge = tokens[1]
        result = parking.getRNumber_withDAge(dAge)
        if result == []:red("null")
        else:
            blue(str(result))

testCase.close()

if os.path.exists(dbFile):os.remove(dbFile)
