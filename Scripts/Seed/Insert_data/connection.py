import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('en_IN')
random.seed(42)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Giribaba@1968",
    database="retail_erp"
)
cursor = conn.cursor()

for i in range(1, 101):
    cursor.execute("""
        INSERT IGNORE INTO units_of_measure (uom_code, uom_name)
        VALUES (%s, %s)
    """, (f"UOM{i}", fake.word()))

