from datetime import *
import logging

import mysql
import yaml
from mysql import connector

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("MySQL_Driver")
logger_mysql = logging.getLogger("MySQL_Driver")

LCT = ""

with open("config.yaml", "r"):
    with open('config.yaml', 'r') as file:
        loadedfile = yaml.safe_load(file)
        MySQLHOST = loadedfile['mysql_ip']
        MySQLPORT = loadedfile['mysql_port']
        MySQLUSER = loadedfile['mysql_user']
        MySQLPASS = loadedfile['mysql_password']
        MySQLDATABASE = loadedfile['mysql_general_database']

DB = mysql.connector.connect(
    host=MySQLHOST,
    port=MySQLPORT,
    user=MySQLUSER,
    password=MySQLPASS,
    database=MySQLDATABASE)


def startdbs():
    FAILSAVE()
    try:
        DB.connect()
    except Exception as e:
        logger.error(f"Помилка при підключенні основної бази данних.\nВиключення: {e}")
        return False
    else:
        logger_mysql.info("Основна база данних підключена!")
    return True

def REstartDBs():
    try:
        DB.connect()
    except Exception as e:
        logger.error(f"FALLBACK: Помилка при підключенні основної бази данних.\nВиключення: {e}")
        return False
    else:
        logger_mysql.info("FALLBACK: Перепідключення успішне")
    return True

def closedbs():
    try:
        DB.connect()
    except Exception as e:
        logger.error(f"Помилка при відключенні основної бази данних.\nВиключення: {e}")
        return False
    else:
        logger_mysql.info("Основна база данних відключена!")


def sendSQL():
    FAILSAVE()
    cursor = DB.cursor()
    return cursor


def executeSQL():
    FAILSAVE()
    cursor = DB.cursor()
    return cursor


def DBCommit():
    try:
        DB.commit()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції DBCommit. DEBUG:\nException: {e}")


# FALLSAVE

def FAILSAVE():
    global LCT
    timenow = datetime.now()
    if len(LCT) == 0:
        LCT = timenow.strftime("%d/%m/%y %H:%M:%S.%f")
        print(f"DNNW: {timenow}")
        print(f"LCT: {LCT}")
        return
    timeLCT = datetime.strptime(LCT, "%d/%m/%y %H:%M:%S.%f")
    diftime = timenow - timeLCT
    print(f"DIFTIME: {diftime}")
    if diftime.total_seconds() > 28000:
        print("RECONECT")
        REstartDBs()
    else:
        print(f"NREC, DIFTIME: {diftime.total_seconds()}/28000")
    LCT = timenow.strftime("%d/%m/%y %H:%M:%S.%f")

