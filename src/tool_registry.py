from tools import *

TOOLS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
    "power": power,
    "execute_sql": execute_sql,
    "get_sql_schema": get_sql_schema
}

if __name__ == "__main__":
    print(TOOLS)
    res = TOOLS["add"]({"x":6, "y":7})