

import os
import pyodbc, struct
from azure import identity
from sqlalchemy import create_engine, text

uami2_clientID="8718f41f-38f7-4fb9-ba85-aabe535ec5f1"
# connection_string = f"Driver={ODBC Driver 18 for SQL Server};Server=tcp:server201124.database.windows.net,1433;Database=db201124;Uid={uami2_clientID};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryIntegrated"
# connection_string = 'Server=tcp:server201124.database.windows.net,1433;Initial Catalog=db201124;Persist Security Info=False;User ID=8718f41f-38f7-4fb9-ba85-aabe535ec5f1;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Authentication="Active Directory Managed Identity";'

server = "tcp:server201124.database.windows.net"
port = 1433
database = "db201124"
client_id = uami2_clientID
authentication = 'ActiveDirectoryIntegrated'
# authentication = 'ActiveDirectoryMsi'
connString = os.environ["AZURE_SQL_CONNECTIONSTRING"]
connString = f'Driver={{ODBC Driver 18 for SQL Server}};Server={server},{port};Database={database};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'


def get_conn():
    # credential = identity.ManagedIdentityCredential(client_id="8718f41f-38f7-4fb9-ba85-aabe535ec5f1")
    credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    # token_bytes = credential.get_token("https://database.windows.net/").token.encode("UTF-16-LE")
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    conn = pyodbc.connect(connString, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn

# conn = get_conn()

# engine = create_engine(conn, echo=True)    
# sql = text(f"select * from dbo.ciudades where ciudad=madrid")
with get_conn() as connection:
    cursor = connection.cursor()
    cursor.execute("select * from dbo.ciudades where nombre='madrid' ")
    rows = cursor.fetchall()

    # cursor = conn.cursor()
    # result = cursor.execute("select * from dbo.ciudades where ciudad='madrid' ").fetchall()

print(rows)
# llamada simple

# credential with uami2_clientID
# get conn string