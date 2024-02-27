import colorama
from colorama import Fore
colorama.init(autoreset=True)
import MySQLdb
import asyncio

#================================================================#
#              🇵🇪 SINS CHK 🇵🇪  - Conexión General                 #
#================================================================#

# ====================== Conexión Remota ====================== #
DB_HOST_ = '' 
DB_USER_ = '' 
DB_PASS_ = '' 
DB_NAME_ = ''
DB_TABLE_ = ''
DB_PUERTO_ = 21630
# ====================== Conexión Local ======================= #
DB_HOST = 'localhost' 
DB_USER = '' 
DB_PASS = '' 
DB_NAME = '' 
DB_TABLE =''
# ============================================================= #

async def run_query(query=''): 
    datos = [DB_HOST_, DB_USER_, DB_PASS_, DB_NAME_, DB_PUERTO_] 
    
    conn = MySQLdb.connect(*datos) # Conectar a la base de datos 
    cursor = conn.cursor()         # Crear un cursor 
    cursor.execute(query)          # Ejecutar una consulta 

    if query.upper().startswith('SELECT'): 
        data = cursor.fetchone()   # Traer los resultados de un select 
    else: 
        conn.commit()              # Hacer efectiva la escritura de datos 
        data = None 
    
    cursor.close()                 # Cerrar el cursor 
    conn.close()                   # Cerrar la conexión 

    await asyncio.sleep(0)

    return data

async def run_query_local(query=''): 
    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
    
    conn = MySQLdb.connect(*datos) # Conectar a la base de datos 
    cursor = conn.cursor()         # Crear un cursor 
    cursor.execute(query)          # Ejecutar una consulta 

    if query.upper().startswith('SELECT'): 
        data = cursor.fetchone()   # Traer los resultados de un select 
    else: 
        conn.commit()              # Hacer efectiva la escritura de datos 
        data = None 
    
    cursor.close()                 # Cerrar el cursor 
    conn.close()                   # Cerrar la conexión 

    await asyncio.sleep(0)

    return data

#================================================================#
#                       Consultas GateWays                       #
#================================================================#

async def actualizarConsultando(user, valor):
    query = f"UPDATE `{DB_TABLE_}` SET `Usando` = '{valor}' WHERE `{DB_TABLE_}`.`UserTelegram` = '{user}';"
    await run_query(query)

async def restarCreditos(user, Creditos):
    query = f"UPDATE {DB_TABLE_} SET Creditos='{Creditos}' WHERE UserTelegram = '{user}'"
    await run_query(query)

async def CreditosChk(user):
    query = f"SELECT Creditos FROM {DB_TABLE_} WHERE UserTelegram = '{user}';"

    creditosConsulta = await run_query(query)
    print(f" {Fore.LIGHTGREEN_EX}[↳] {user} tiene {Fore.LIGHTWHITE_EX}{creditosConsulta[0]}{Fore.LIGHTGREEN_EX} créditos.")

    return int(creditosConsulta[0])