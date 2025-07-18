import asyncio
import asyncpg

from config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT, SCHEMA_PATH

# actions
def add(input: dict):
    """
    Takes a dictionary with two numbers and returns their sum (x + y).
    Example input: {"x": 5, "y": 3}
    """
    x = input["x"]
    y = input["y"]
    return x + y

def subtract(input: dict):
    """
    Takes a dictionary with two numbers and returns their difference (x - y).
    Example input: {"x": 10, "y": 4}
    """
    x = input["x"]
    y = input["y"]
    return x - y

def multiply(input: dict):
    """
    Takes a dictionary with two numbers and returns their product (x * y).
    Example input: {"x": 3, "y": 4}
    """
    x = input["x"]
    y = input["y"]
    return x * y

def divide(input: dict):
    """
    Takes a dictionary with two numbers and returns the result of dividing the first by the second (x / y).
    Example input: {"x": 10, "y": 2}
    """
    x = input["x"]
    y = input["y"]
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

def power(input: dict):
    """
    Takes a dictionary with two numbers and returns the result of raising the first to the power of the second (x ** y).
    Example input: {"x": 2, "y": 3}
    """
    x = input["x"]
    y = input["y"]
    return x ** y

def get_sql_schema(path=""):
    """
    Takes input as "" empty string
    Provides the sql schema for the CRM database. ALWAYS run this tool before creating an SQL query.
    Use this tool before execute_sql.
    
    """
    path=SCHEMA_PATH
    with open(path, "r") as f:
        db_schema = f.read()
    return db_schema

async def execute_sql(query):
    """
    Executes a given SQL query asynchronously on the configured PostgreSQL database 
    and returns the result as a list of dictionaries.
    execute_sql depends on the output get_sql_schema
    Before using this tool, use get_sql_schema to get the schema of the CRM database.

    Input:
        query (str): A valid SQL query string to be executed.

    Example Input:
        Input:
            "SELECT * FROM customers WHERE id = 1"
    """
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT
    )
    result = await conn.fetch(query)
    await conn.close()
    return [dict(record) for record in result]

if __name__ == "__main__":
    res = asyncio.run(execute_sql(query="SELECT * FROM customers LIMIT 1;"))
    print(res)