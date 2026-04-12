'''Run it once'''

import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
from datetime import date, timedelta
import sys

fake = Faker('en_IN')
random.seed(42)
Faker.seed(42)

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Giribaba@1968",
    "database": "retail_erp",
}

# ───────────────── CONNECTION ─────────────────
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("✅ Connected to MySQL")
            return conn
    except Error as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)

def rand_date(start_year=2023, end_year=2026):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

# ───────────────── MASTER DATA ─────────────────
def insert_master(cursor):

    cursor.execute("INSERT IGNORE INTO units_of_measure (uom_code,uom_name) VALUES ('PCS','Pieces'),('KG','Kg'),('LTR','Litre')")
    
    cursor.execute("INSERT IGNORE INTO categories (category_code,category_name) VALUES ('FOOD','Food'),('ELEC','Electronics')")

    cursor.execute("INSERT IGNORE INTO warehouses (warehouse_code,warehouse_name) VALUES ('WH1','Main WH'),('WH2','Backup WH')")

    cursor.execute("SELECT warehouse_id FROM warehouses")
    wh_ids=[x[0] for x in cursor.fetchall()]

    cursor.execute("INSERT IGNORE INTO stores (store_code,store_name,warehouse_id) VALUES ('ST1','Store1',%s),('ST2','Store2',%s)",(wh_ids[0],wh_ids[1]))

    cursor.execute("INSERT IGNORE INTO employees (employee_code,first_name,last_name,role) VALUES ('E1','A','B','CASHIER'),('E2','X','Y','MANAGER')")

    cursor.execute("INSERT IGNORE INTO customers (customer_code,customer_name) VALUES ('C1','Cust1'),('C2','Cust2')")

    cursor.execute("INSERT IGNORE INTO suppliers (supplier_code,supplier_name) VALUES ('S1','Supp1'),('S2','Supp2')")

    cursor.execute("SELECT category_id FROM categories")
    cat_ids=[x[0] for x in cursor.fetchall()]

    cursor.execute("SELECT uom_id FROM units_of_measure")
    uom_ids=[x[0] for x in cursor.fetchall()]

    products=[]
    for i in range(1,21):
        products.append((f"SKU{i}",f"Product{i}",random.choice(cat_ids),random.choice(uom_ids),"1001",random.uniform(10,500),random.uniform(20,800),10))

    cursor.executemany("""
        INSERT INTO products (sku,product_name,category_id,uom_id,hsn_code,purchase_price,selling_price,reorder_level)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """,products)

# ───────────────── FETCH IDS ─────────────────
def fetch_ids(cursor):
    cursor.execute("SELECT product_id FROM products")
    products=[x[0] for x in cursor.fetchall()]

    cursor.execute("SELECT warehouse_id FROM warehouses")
    wh=[x[0] for x in cursor.fetchall()]

    cursor.execute("SELECT store_id FROM stores")
    stores=[x[0] for x in cursor.fetchall()]

    cursor.execute("SELECT employee_id FROM employees")
    emp=[x[0] for x in cursor.fetchall()]

    cursor.execute("SELECT customer_id FROM customers")
    cust=[x[0] for x in cursor.fetchall()]

    cursor.execute("SELECT supplier_id FROM suppliers")
    sup=[x[0] for x in cursor.fetchall()]

    return products,wh,stores,emp,cust,sup

# ───────────────── DIRTY PURCHASE ─────────────────
def insert_purchase(cursor, products, wh, sup, emp):

    for i in range(50):

        cursor.execute("""
        INSERT INTO purchase_orders (po_number,supplier_id,warehouse_id,po_status,order_date,total_amount,created_by)
        VALUES (%s,%s,%s,'RECEIVED',%s,0,%s)
        """,(f"PO{i}",random.choice(sup),random.choice(wh),rand_date(),random.choice(emp)))

        po_id=cursor.lastrowid

        total=0

        for _ in range(3):
            p=random.choice(products)

            qty_o=random.uniform(10,100)

            # DIRTY: received > ordered
            qty_r=qty_o * random.uniform(0.8,1.5)

            price=random.uniform(10,200)

            total+=qty_o*price

            cursor.execute("""
            INSERT INTO purchase_order_items (po_id,product_id,quantity_ordered,quantity_received,unit_cost)
            VALUES (%s,%s,%s,%s,%s)
            """,(po_id,p,qty_o,qty_r,price))

        # DIRTY: wrong PO total
        cursor.execute("UPDATE purchase_orders SET total_amount=%s WHERE po_id=%s",
                       (total + random.uniform(-500,500),po_id))

# ───────────────── DIRTY INVENTORY ─────────────────
def insert_inventory(cursor, products, wh):

    for p in products:
        for w in wh:

            qty=random.uniform(-50,200)  # negative stock

            cursor.execute("""
            INSERT INTO inventory_stock (product_id,warehouse_id,quantity_on_hand)
            VALUES (%s,%s,%s)
            ON DUPLICATE KEY UPDATE quantity_on_hand=%s
            """,(p,w,qty,qty))

# ───────────────── DIRTY POS ─────────────────
def insert_pos(cursor, products, stores, emp, cust):

    for i in range(200):

        cursor.execute("""
        INSERT INTO pos_sales (bill_number,store_id,cashier_id,customer_id,sale_date,subtotal_amount,discount_amount,tax_amount,total_amount,payment_method)
        VALUES (%s,%s,%s,%s,%s,0,0,0,0,'CASH')
        """,(f"B{i}",random.choice(stores),random.choice(emp),
             random.choice(cust) if random.random()>0.5 else None,
             rand_date()))

        sid=cursor.lastrowid

        sub=0

        for _ in range(random.randint(1,5)):
            p=random.choice(products)

            qty=random.uniform(-2,5)  # negative qty

            price=random.uniform(10,500)

            total=qty*price

            cursor.execute("""
            INSERT INTO pos_sale_items (sale_id,product_id,quantity,unit_price,total_price)
            VALUES (%s,%s,%s,%s,%s)
            """,(sid,p,qty,price,total))

            sub+=total

        # DIRTY: wrong total
        cursor.execute("""
        UPDATE pos_sales SET subtotal_amount=%s,total_amount=%s WHERE sale_id=%s
        """,(sub, sub + random.uniform(-100,100), sid))

# ───────────────── MAIN ─────────────────
def main():

    conn=get_connection()
    cursor=conn.cursor()

    try:
        print("Inserting master data...")
        insert_master(cursor)
        conn.commit()

        products,wh,stores,emp,cust,sup=fetch_ids(cursor)

        print("Inserting dirty purchase...")
        insert_purchase(cursor,products,wh,sup,emp)
        conn.commit()

        print("Inserting dirty inventory...")
        insert_inventory(cursor,products,wh)
        conn.commit()

        print("Inserting dirty POS...")
        insert_pos(cursor,products,stores,emp,cust)
        conn.commit()

        print("✅ DIRTY DATA INSERTED SUCCESSFULLY")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")

    finally:
        cursor.close()
        conn.close()
        print("Connection closed")

if __name__ == "__main__":
    main()