import logging
import os
import sqlite3
import json

class Device:
    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def importdb(self, dbfile):
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
        self.user_id = data[num][0]['User_id']
        self.device_id = data[num][1]['Device_id']
        self.role = data[num][0]['Roles']

    def check_user_id(self):
        if self.user_id in self.user_id_list:
            self.logger.error("The user id has been recorded.")
        elif not isinstance(self.user_id, int):
            self.logger.error("The format of user id is wrong.")
        else:
            return True

    def check_device_id(self):
        if self.device_id in self.device_id_list:
            self.logger.error("The device id has been recorded.")
        elif not isinstance(self.device_id, int):
            self.logger.error("The format of device id is wrong.")
        else:
            return True   

    def check_role(self):
        roles = ["Patient", "Doctor", "Nurse", "AI_Developer", "Administrator"]
        if self.role not in roles:
            self.logger.error("Your role is not acceptable.")
            print("no")
        else:
            return True

    def create_device(self, data, dbfile):
        #if(self.check_user_id() & self.check_device_id() & self.check_role()):
        Users = tuple(list(data[0].values()))
        Devices = tuple(list(data[1].values()))
        Measurements = tuple(list(data[2].values()))
        Assignments = tuple(list(data[3].values()))

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

    def control(self,dbfile):
        keys = list(data.keys())
        for key in keys:
            print("\n","control start", key)
            self.get_device(key)
            a = self.check_user_id()
            b = self.check_device_id()
            c = self.check_role()
            if (a == b == c == True):
                self.create_device(data[key],dbfile)
                print("your information is recorded succesfully")
            else:
                print("There is something wrong")
                continue
            print("control end",self.user_id,"\n" )

if __name__ == '__main__':
    dm = Device()
    dm.importdb("table.db")

    f = open("data.json") # data.json
    data = json.loads(f.read())

    dm.control("table.db")
    # keys = data.keys()
    # for key in keys():
    #     dm.get_device(key)

    # dm.check_user_id()
    # dm.check_device_id()
    # dm.check_role()
    # if (self.check_user_id() & self.check_device_id() & self.check_role()):
    #     dm.create_device()
