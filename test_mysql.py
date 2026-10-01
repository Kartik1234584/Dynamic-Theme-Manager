import mysql.connector

pwds = ["", "root", "password", "admin", "1234"]
for p in pwds:
    try:
        mysql.connector.connect(host='127.0.0.1', user='root', password=p)
        print("SUCCESS:", p)
        break
    except Exception as e:
        print("FAILED:", p, e)
