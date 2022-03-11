import logging
import os
import sqlite3
import json
# import table

class Device:
    def __init__(self, jsfile):
        logging.basicConfig(format='%(levelname)s - %(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        f = open(jsfile) # data.json
        self.data = json.loads(f.read())

    def importdb(self, dbfile):
        # first step is to initialize
        if os.path.exists(dbfile):
            os.remove(dbfile)
        os.system('python table.py')

        # get the data of the database
        con = sqlite3.connect(dbfile) # table.db
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM Storage')

        #self.premission = []
        self.user_id_list = []
        self.device_id_list = []
        #self.role = []

        for row in cur:
            # self.premission_list.append(row['Premission'])
            self.user_id_list.append(row['User_id'])
            self.device_id_list.append(row['Device_id'])
            # self.role_list.append(row['Roles'])

    def get_device(self, num):
        # f = open(jsonfile) # data.json
        # data = json.loads(f.read())
        int(num)
        self.user_id = self.data[num][0]['User_id']
        self.device_id = self.data[num][1]['Device_id']
        self.role = self.data[num][0]['Roles']

    def check_user_id(self):
        if self.user_id in self.user_id_list:
            #print("--print----: The user id has been recorded.")
            self.logger.error("The user id has been recorded.")
        elif not isinstance(self.user_id, int):
            #print("--print----: The format of user id is wrong.")
            self.logger.error("The format of user id is wrong.")
        else:
            return True

    def check_device_id(self):
        if self.device_id in self.device_id_list:
            #print("--print----: The device id has been recorded.")
            self.logger.error("The device id has been recorded.")
        elif not isinstance(self.device_id, int):
            #print("--print----: The format of device id is wrong.")
            self.logger.error("The format of device id is wrong.")
        else:
            return True   

    def check_role(self):
        roles = ["Patient", "Doctor", "Nurse", "AI_Developer", "Administrator"]
        if self.role not in roles:
            #print("--print----: Your role is not acceptable.")
            self.logger.error("Your role is not acceptable.")
            #print("no")
        else:
            return True

    def create_device(self, dt, dbfile):
        #if(self.check_user_id() & self.check_device_id() & self.check_role()):
        Users = tuple(list(dt[0].values()))
        Devices = tuple(list(dt[1].values()))
        Measurements = tuple(list(dt[2].values()))
        Assignments = tuple(list(dt[3].values()))

        conn = sqlite3.connect(dbfile) # table.db
        cur = conn.cursor()

        sql_statement = 'INSERT INTO Users VALUES (?, ?, ?, ?, ?)'
        cur.executemany(sql_statement, [Users])

        sql_statement = 'INSERT INTO Devices VALUES (?, ?, ?, ?, ?)'
        cur.executemany(sql_statement, [Devices])

        sql_statement = 'INSERT INTO Measurements VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur.executemany(sql_statement, [Measurements])
        
        sql_statement = 'INSERT INTO Assignments VALUES (?, ?, ?, ?)'
        cur.executemany(sql_statement, [Assignments])
    
    def control(self, dbfile):
        # f = open(jsfile) # data.json
        # self.data = json.loads(f.read())

        self.importdb(dbfile)

        keys = list(self.data.keys())
        for key in keys:
            self.logger.info(f"number {key}'s data")
            #print("control start", key)
            self.get_device(key)
            a = self.check_user_id()
            b = self.check_device_id()
            c = self.check_role()
            if (a == b == c == True):
                self.create_device(self.data[key],dbfile)
                self.logger.info(f"your information is recorded succesfully\n")
                #print("your information is recorded succesfully\n")
            else:
                self.logger.info(f"The user's information failed to be recorded.\n")
                #print("There is something wrong\n")
                continue
            
            print("\n\ncontrol end, the user id is ",self.user_id,"\n" )

if __name__ == '__main__':
    dm = Device(jsfile) # "data.json"
    # dm.importdb("table.db")

    # f = open("data.json") # data.json
    # data = json.loads(f.read())

    dm.control(dbfile) # "table.db"
