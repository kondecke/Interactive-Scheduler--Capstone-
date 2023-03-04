import mysql.connector
import sshtunnel
import config
class dbConnection():
    def __init__(self): 
        self.sshHost = config.SSH_HOST
        self.sshUser = config.SSH_USER
        self.sshPwd = config.SSH_PWD
        self.dbUser = config.DB_USER
        self.dbPwd = config.DB_PWD
        self.dbHost = config.DB_HOST_NAME
        self.dbName = config.DB_NAME

    def connect(self):
        sshtunnel.SSH_TIMEOUT = 5.0
        sshtunnel.TUNNEL_TIMEOUT = 5.0 
        with sshtunnel.SSHTunnelForwarder(
            (self.sshHost),
            ssh_username=self.sshUser, ssh_password=self.sshPwd, 
            remote_bind_address=(self.dbHost, 3306)
            ) as tunnel: 
                cnxn = mysql.connector.connect(user=self.dbUser, password=self.dbPwd, host='127.0.0.1', port=tunnel.local_bind_port, db=self.dbName,)
                return cnxn
    def printDebug(self):
         print(self.sshUser)  
db = dbConnection()
db.connect()
db.printDebug()

            