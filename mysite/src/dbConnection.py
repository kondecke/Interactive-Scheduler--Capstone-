import mysql.connector
import os
import sshtunnel

class dbConnection():
    def __init__(self): 
        self.sshHost = os.getenv("SSH_HOST")
        self.sshUser = os.getenv("SSH_USER")
        self.sshPwd = os.getenv("SSH_PWD")
        self.dbUser = os.getenv("DB_USER")
        self.dbPwd = os.getenv("DB_PWD")
        self.dbHost = os.getenv("DB_HOST_NAME")
        self.dbName = os.getenv("DB_NAME")

    def connect(self):
        sshtunnel.SSH_TIMEOUT = 5.0
        sshtunnel.TUNNEL_TIMEOUT = 5.0 
        with sshtunnel.SSHTunnelForwarder(
            (self.sshHost),
            ssh_username=self.sshUser, ssh_password=self.sshPwd, 
            remote_bind_address=(self.dbHost, 3306)
            ) as tunnel: 
                cnxn = mysql.connector.connect(user=self.dbUser, password=self.dbPwd, host=self.dbHost, port=tunnel.local_bind_port, db=self.dbName,)
                return cnxn
    def printDebug(self):
         print(self.sshUser)  
db = dbConnection()
db.printDebug()

            