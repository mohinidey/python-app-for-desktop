import mysql.connector

class DBhelper:
    def __init__(self):
        try:

             self._connection=mysql.connector.connect(host="127.0.0.1", user="root",password="",database="tinderb3")
             self._cursor=self._connection.cursor()
             print("Connected to database")
        except:
            print("Could not connect to database")
            exit(0)

    def search(self,key1,value1,key2,value2,table):
        self._cursor.execute("""
        SELECT * FROM `{}` WHERE `{}` LIKE '{}' AND `{}` LIKE '{}'
        """.format(table,key1,value1,key2,value2))
        data=self._cursor.fetchall()
        return data
    
    def searchOne(self,key1,value1,table,type):
        self._cursor.execute("""
        SELECT * FROM `{}` WHERE `{}` {} '{}' """.format(table,key1,type,value1))
        data=self._cursor.fetchall()
        return data

    def insert(self,insertDict,table,mode=0):
        #INSERT INTO `users` (`name`,`email`,`password`,`gender`,`age`,`city`) VALUES ('NITISH','nitish@gmail.com','male','22','mumbai')"


        colValue=""
        dataValue=""
        for i in insertDict:
            colValue=colValue + "`" + i + "`,"
            dataValue=dataValue + "'" + insertDict[i] + "',"
        if mode==0:
            colValue=colValue+"`dp`"
            dataValue=dataValue+"'nodp.png'"
        else:
            colValue=colValue[:-1]
            dataValue=dataValue[:-1]
        query="INSERT INTO `{0}` ({1}) VALUES ({2})".format(table,colValue,dataValue)

        try:
            self._cursor.execute(query)
            self._connection.commit()
            
            return 1
        except:
            return 0
    def setDp(self,filename,table1,user_id,dp,id_value):
        self._cursor.execute("""update  `{}` set {}= '{}'  WHERE {} ={}""".format(table1,dp,filename,user_id,id_value))
    def searchMyProposals(self,table1,key1,juliet_id,table2,romeo_id,value1):
        self._cursor.execute("""SELECT * from `{}` where {} in (SELECT {} FROM `{}` WHERE {}={})""".format(table1,key1,juliet_id,table2,romeo_id,value1))
        data=self._cursor.fetchall()
        return data 

    def searchMyRequests(self,table1,key1,romeo_id,table2,juliet_id,value1):
        self._cursor.execute("""SELECT * from `{}` where {} in (SELECT {} FROM `{}` WHERE {}={})""".format(table1,key1,romeo_id,table2,juliet_id,value1))
        data=self._cursor.fetchall()
        return data

    def searchMyMatches(self,table1,key1,romeo_id,table2,juliet_id,value1):
        #SELECT * from users where user_id in (SELECT p1.juliet_id  FROM `proposals` p1, `proposals` p2 where p1.romeo_id = p2 .juliet_id and p2.romeo_id = p1 .juliet_id and p1.romeo_id=12)
        self._cursor.execute("""SELECT * from `{0}` where {1} in (SELECT p1.{3}  FROM `{4}` p1, `{4}` p2 where p1.{2} = p2 .{3} and p1.{3} = p2 .{2} and p1.{2}={5})
        """.format(table1,key1,romeo_id,juliet_id,table2,value1))
        data=self._cursor.fetchall()
        return data
