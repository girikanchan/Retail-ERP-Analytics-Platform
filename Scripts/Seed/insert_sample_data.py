'''Run it once'''

"""
=============================================================
  retail_erp  —  Sample Data Insertion Script
  Connector : mysql-connector-python
  Volume    : Medium (~2000 rows)
  Host      : localhost
=============================================================
  Install dependency:
      pip3 install mysql-connector-python faker  --break-system-packages
  Run:
      python3 insert_sample_data.py
=============================================================
"""

import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
from datetime import date, timedelta
import sys

fake = Faker('en_IN')
random.seed(42)
Faker.seed(42)

# ── CONNECTION CONFIG ─────────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",         
    "password": "Giribaba@1968",       
    "database": "retail_erp",
}

# ── HELPERS ───────────────────────────────────────────────────────────────────
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("✅  Connected to MySQL — retail_erp")
            return conn
    except Error as e:
        print(f"❌  Connection failed: {e}")
        sys.exit(1)

def execute_many(cursor, sql, data, label):
    try:
        cursor.executemany(sql, data)
        print(f"   ✔  {label:45s}  {len(data):>5} rows")
    except Error as e:
        print(f"   ✘  {label} — ERROR: {e}")
        raise

def rand_date(start_year=2023, end_year=2024):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 1 — FOUNDATION
# ══════════════════════════════════════════════════════════════════════════════
def insert_units_of_measure(cursor):
    data = [("PCS","Pieces"),("KG","Kilogram"),("LTR","Litre"),
            ("MTR","Metre"),("BOX","Box"),("PKT","Packet"),
            ("DOZ","Dozen"),("GM","Gram")]
    execute_many(cursor,
        "INSERT IGNORE INTO units_of_measure (uom_code,uom_name) VALUES (%s,%s)",
        data, "units_of_measure")
    cursor.execute("SELECT uom_id,uom_code FROM units_of_measure")
    return {r[1]:r[0] for r in cursor.fetchall()}

def insert_categories(cursor):
    parents = [(None,"FOOD","Food & Grocery"),(None,"ELEC","Electronics"),
               (None,"APPL","Home Appliances"),(None,"CLTH","Clothing"),
               (None,"HEALTH","Health & Pharma")]
    sql = "INSERT IGNORE INTO categories (parent_id,category_code,category_name) VALUES (%s,%s,%s)"
    execute_many(cursor, sql, parents, "categories (parents)")
    cursor.execute("SELECT category_id,category_code FROM categories WHERE parent_id IS NULL")
    pm = {r[1]:r[0] for r in cursor.fetchall()}
    children = [
        (pm["FOOD"],"DAIRY","Dairy Products"),(pm["FOOD"],"BEVER","Beverages"),
        (pm["FOOD"],"SNACK","Snacks & Namkeen"),(pm["FOOD"],"GRAIN","Grains & Pulses"),
        (pm["ELEC"],"MOBILE","Mobile Phones"),(pm["ELEC"],"LAPTOP","Laptops & Computers"),
        (pm["APPL"],"KITCH","Kitchen Appliances"),(pm["HEALTH"],"VITAM","Vitamins & Supplements"),
    ]
    execute_many(cursor, sql, children, "categories (children)")
    cursor.execute("SELECT category_id,category_code FROM categories")
    return {r[1]:r[0] for r in cursor.fetchall()}

def insert_employees(cursor):
    roles = ["CASHIER","STORE_KEEPER","MANAGER","PURCHASE_OFFICER","WAREHOUSE_STAFF"]
    data = [(f"EMP{i:04d}",fake.first_name(),fake.last_name(),random.choice(roles))
            for i in range(1,21)]
    execute_many(cursor,
        "INSERT IGNORE INTO employees (employee_code,first_name,last_name,role) VALUES (%s,%s,%s,%s)",
        data, "employees")
    cursor.execute("SELECT employee_id FROM employees")
    return [r[0] for r in cursor.fetchall()]

def insert_customers(cursor):
    data = [(f"CUST{i:04d}",fake.name(),fake.phone_number()[:20],fake.email(),
             fake.address().replace("\n",", ")[:200],
             f"29AABCT{random.randint(1000,9999)}R{random.randint(1,9)}Z{random.randint(1,9)}"
             if random.random()>0.5 else None)
            for i in range(1,51)]
    execute_many(cursor,
        "INSERT IGNORE INTO customers (customer_code,customer_name,phone,email,address,gstin) VALUES (%s,%s,%s,%s,%s,%s)",
        data, "customers")
    cursor.execute("SELECT customer_id FROM customers")
    return [r[0] for r in cursor.fetchall()]

def insert_suppliers(cursor):
    names = ["Hindustan Unilever Ltd","ITC Limited","Nestlé India","Amul Dairy",
             "Britannia Industries","Parle Products","Samsung Electronics India",
             "LG Electronics India","Tata Consumer Products","Dabur India Ltd",
             "Marico Ltd","Godrej Consumer Products"]
    terms = ["NET30","NET45","NET60","IMMEDIATE","NET15"]
    data  = [(f"SUP{i:04d}",n,fake.name(),fake.phone_number()[:20],fake.email(),
              fake.address().replace("\n",", ")[:200],
              f"29AABCT{random.randint(1000,9999)}R{random.randint(1,9)}Z{random.randint(1,9)}",
              random.choice(terms))
             for i,n in enumerate(names,1)]
    execute_many(cursor,
        "INSERT IGNORE INTO suppliers (supplier_code,supplier_name,contact_person,phone,email,address,gstin,payment_terms) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
        data, "suppliers")
    cursor.execute("SELECT supplier_id FROM suppliers")
    return [r[0] for r in cursor.fetchall()]

def insert_warehouses(cursor):
    data = [("WH001","Hyderabad Central Warehouse","Kukatpally, Hyderabad"),
            ("WH002","Mumbai Distribution Centre","Andheri East, Mumbai"),
            ("WH003","Bengaluru Fulfillment Hub","Whitefield, Bengaluru"),
            ("WH004","Delhi North Warehouse","Narela, New Delhi")]
    execute_many(cursor,
        "INSERT IGNORE INTO warehouses (warehouse_code,warehouse_name,address) VALUES (%s,%s,%s)",
        data, "warehouses")
    cursor.execute("SELECT warehouse_id FROM warehouses")
    return [r[0] for r in cursor.fetchall()]

def insert_stores(cursor, wh_ids):
    data = [("ST001","Hyderabad Banjara Hills",wh_ids[0]),
            ("ST002","Hyderabad Jubilee Hills",wh_ids[0]),
            ("ST003","Mumbai Andheri",wh_ids[1]),
            ("ST004","Mumbai Powai",wh_ids[1]),
            ("ST005","Bengaluru Koramangala",wh_ids[2]),
            ("ST006","Delhi Connaught Place",wh_ids[3])]
    execute_many(cursor,
        "INSERT IGNORE INTO stores (store_code,store_name,warehouse_id) VALUES (%s,%s,%s)",
        data, "stores")
    cursor.execute("SELECT store_id FROM stores")
    return [r[0] for r in cursor.fetchall()]

def insert_products(cursor, cat_map, uom_map):
    rows = [
        ("SKU0001","Amul Full Cream Milk 1L","DAIRY","LTR","0401",48.00,58.00,50),
        ("SKU0002","Amul Butter 500g","DAIRY","GM","0405",220.00,260.00,30),
        ("SKU0003","Mother Dairy Curd 400g","DAIRY","GM","0403",38.00,45.00,40),
        ("SKU0004","Nestlé Milkmaid 400g","DAIRY","GM","0402",85.00,98.00,25),
        ("SKU0005","Tata Tea Gold 500g","BEVER","GM","0902",195.00,235.00,30),
        ("SKU0006","Nescafé Classic 100g","BEVER","GM","2101",210.00,250.00,20),
        ("SKU0007","Tropicana Orange 1L","BEVER","LTR","2009",95.00,115.00,25),
        ("SKU0008","Bisleri Water 1L","BEVER","LTR","2201",12.00,20.00,100),
        ("SKU0009","Lays Classic Salted 90g","SNACK","GM","1905",15.00,20.00,60),
        ("SKU0010","Britannia Good Day 200g","SNACK","GM","1905",28.00,35.00,50),
        ("SKU0011","Haldiram Bhujia 400g","SNACK","GM","1905",88.00,105.00,30),
        ("SKU0012","Kurkure Masala Munch 90g","SNACK","GM","1905",16.00,20.00,60),
        ("SKU0013","India Gate Basmati Rice 5kg","GRAIN","KG","1006",380.00,449.00,20),
        ("SKU0014","Tata Sampann Toor Dal 1kg","GRAIN","KG","0713",95.00,115.00,30),
        ("SKU0015","Aashirvaad Wheat Flour 5kg","GRAIN","KG","1101",210.00,250.00,20),
        ("SKU0016","Samsung Galaxy A54 5G","MOBILE","PCS","8517",28000.00,32999.00,5),
        ("SKU0017","Redmi Note 13 Pro","MOBILE","PCS","8517",18000.00,21999.00,5),
        ("SKU0018","realme 12 Pro Plus","MOBILE","PCS","8517",22000.00,26999.00,5),
        ("SKU0019","HP Laptop 15s Intel i5","LAPTOP","PCS","8471",42000.00,49999.00,3),
        ("SKU0020","Lenovo IdeaPad Slim 3","LAPTOP","PCS","8471",38000.00,44999.00,3),
        ("SKU0021","Prestige Pressure Cooker 5L","KITCH","PCS","7323",1400.00,1799.00,10),
        ("SKU0022","Bajaj Mixer Grinder 750W","KITCH","PCS","8509",2200.00,2799.00,8),
        ("SKU0023","Philips Air Fryer 4.1L","KITCH","PCS","8516",5500.00,6999.00,5),
        ("SKU0024","Himalaya Ashvagandha 60 Tabs","VITAM","PCS","3004",140.00,175.00,15),
        ("SKU0025","Centrum Adult Multivitamin 30s","VITAM","PCS","3004",320.00,399.00,10),
    ]
    data = [(sku,name,cat_map[cat],uom_map[uom],hsn,pp,sp,rl)
            for sku,name,cat,uom,hsn,pp,sp,rl in rows]
    execute_many(cursor,
        "INSERT IGNORE INTO products (sku,product_name,category_id,uom_id,hsn_code,purchase_price,selling_price,reorder_level) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
        data, "products")
    cursor.execute("SELECT product_id,sku,purchase_price,selling_price FROM products")
    return {r[1]:{"id":r[0],"pp":float(r[2]),"sp":float(r[3])} for r in cursor.fetchall()}

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — GST
# ══════════════════════════════════════════════════════════════════════════════
def insert_tax_master(cursor):
    data = [("GST 0%",0.00,"IGST"),("CGST 2.5%",2.50,"CGST"),("SGST 2.5%",2.50,"SGST"),
            ("IGST 5%",5.00,"IGST"),("CGST 6%",6.00,"CGST"),("SGST 6%",6.00,"SGST"),
            ("IGST 12%",12.00,"IGST"),("CGST 9%",9.00,"CGST"),("SGST 9%",9.00,"SGST"),
            ("IGST 18%",18.00,"IGST")]
    execute_many(cursor,
        "INSERT IGNORE INTO tax_master (tax_name,tax_percentage,tax_type) VALUES (%s,%s,%s)",
        data, "tax_master")
    cursor.execute("SELECT tax_id,tax_name FROM tax_master")
    return {r[1]:r[0] for r in cursor.fetchall()}

def insert_product_tax_mapping(cursor, prod_map, tax_map):
    data = []
    for i,(sku,pi) in enumerate(prod_map.items(),1):
        n = int(sku[3:])
        if   n <= 15: cgst,sgst = tax_map["CGST 2.5%"],tax_map["SGST 2.5%"]
        elif n <= 20: cgst,sgst = tax_map["CGST 9%"],   tax_map["SGST 9%"]
        elif n <= 23: cgst,sgst = tax_map["CGST 6%"],   tax_map["SGST 6%"]
        else:         cgst,sgst = tax_map["CGST 6%"],   tax_map["SGST 6%"]
        data.append((pi["id"],cgst))
        data.append((pi["id"],sgst))
    execute_many(cursor,
        "INSERT IGNORE INTO product_tax_mapping (product_id,tax_id) VALUES (%s,%s)",
        data, "product_tax_mapping")

def insert_gst_invoice_details(cursor, tax_map):
    cursor.execute("SELECT sale_id,tax_amount FROM pos_sales WHERE tax_amount>0 LIMIT 150")
    sales = cursor.fetchall()
    data  = []
    for sid,ta in sales:
        half = round(float(ta)/2, 2)
        base = round(float(ta)/0.05, 2)
        data.append(("SALE",sid,tax_map["CGST 2.5%"],base,half))
        data.append(("SALE",sid,tax_map["SGST 2.5%"],base,half))
    execute_many(cursor,
        "INSERT INTO gst_invoice_details (reference_type,reference_id,tax_id,taxable_amount,tax_amount) VALUES (%s,%s,%s,%s,%s)",
        data, "gst_invoice_details")

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — REORDER
# ══════════════════════════════════════════════════════════════════════════════
def insert_reorder_rules(cursor, prod_map, wh_ids, sup_ids):
    data = [(pi["id"],wid,random.randint(10,30),random.randint(20,60),
             random.choice(sup_ids),random.randint(3,14))
            for pi in prod_map.values() for wid in wh_ids]
    execute_many(cursor,
        "INSERT IGNORE INTO reorder_rules (product_id,warehouse_id,min_stock_level,reorder_quantity,preferred_supplier_id,lead_time_days) VALUES (%s,%s,%s,%s,%s,%s)",
        data, "reorder_rules")

def insert_supplier_product_rules(cursor, prod_map, sup_ids):
    data = []
    for pi in prod_map.values():
        for rank,sid in enumerate(random.sample(sup_ids,k=min(3,len(sup_ids))),1):
            data.append((sid,pi["id"],rank,
                         round(pi["pp"]*random.uniform(0.88,1.05),2),
                         random.randint(3,21)))
    execute_many(cursor,
        "INSERT IGNORE INTO supplier_product_rules (supplier_id,product_id,priority_rank,unit_cost,lead_time_days) VALUES (%s,%s,%s,%s,%s)",
        data, "supplier_product_rules")

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 4 — PURCHASE CYCLE
# ══════════════════════════════════════════════════════════════════════════════
def insert_purchase_cycle(cursor, prod_map, wh_ids, sup_ids, emp_ids):
    statuses  = ["RECEIVED","RECEIVED","RECEIVED","PARTIAL","SENT"]
    inv_stats = ["PAID","PAID","APPROVED","PENDING"]
    pay_meths = ["BANK_TRANSFER","CHEQUE","UPI","BANK_TRANSFER"]
    skus      = list(prod_map.keys())

    for n in range(1, 61):
        od    = rand_date(2023,2024)
        sid   = random.choice(sup_ids)
        wid   = random.choice(wh_ids)
        stat  = random.choice(statuses)
        eid   = random.choice(emp_ids)
        cursor.execute(
            "INSERT INTO purchase_orders (po_number,supplier_id,warehouse_id,po_status,order_date,expected_delivery_date,total_amount,created_by) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (f"PO{n:05d}",sid,wid,stat,od,od+timedelta(days=random.randint(3,14)),0.00,eid))
        po_id = cursor.lastrowid

        po_total = 0; po_items = []
        for sku in random.sample(skus,k=random.randint(2,5)):
            pi      = prod_map[sku]
            qty_o   = round(random.uniform(10,100),3)
            qty_r   = qty_o if stat=="RECEIVED" else round(qty_o*random.uniform(0.5,0.9),3)
            uc      = round(pi["pp"]*random.uniform(0.92,1.02),2)
            po_total += qty_o*uc
            cursor.execute(
                "INSERT INTO purchase_order_items (po_id,product_id,quantity_ordered,quantity_received,unit_cost) VALUES (%s,%s,%s,%s,%s)",
                (po_id,pi["id"],qty_o,qty_r,uc))
            po_items.append({"poi_id":cursor.lastrowid,"pid":pi["id"],"qr":qty_r,"uc":uc})

        cursor.execute("UPDATE purchase_orders SET total_amount=%s WHERE po_id=%s",(round(po_total,2),po_id))

        if stat in ("RECEIVED","PARTIAL"):
            rd     = od+timedelta(days=random.randint(2,10))
            gs     = "ACCEPTED" if random.random()>0.1 else "REJECTED"
            cursor.execute(
                "INSERT INTO goods_receipt_notes (grn_number,po_id,warehouse_id,received_by,receipt_date,grn_status) VALUES (%s,%s,%s,%s,%s,%s)",
                (f"GRN{n:05d}",po_id,wid,random.choice(emp_ids),rd,gs))
            grn_id = cursor.lastrowid
            for it in po_items:
                qa = it["qr"] if gs=="ACCEPTED" else round(it["qr"]*0.9,3)
                cursor.execute(
                    "INSERT INTO grn_items (grn_id,po_item_id,product_id,quantity_received,quantity_accepted,quantity_rejected,unit_cost) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (grn_id,it["poi_id"],it["pid"],it["qr"],qa,round(it["qr"]-qa,3),it["uc"]))
            ia  = round(po_total*random.uniform(0.98,1.00),2)
            ta  = round(ia*0.18,2)
            ist = random.choice(inv_stats)
            id_ = rd+timedelta(days=random.randint(1,5))
            cursor.execute(
                "INSERT INTO supplier_invoices (supplier_id,po_id,grn_id,invoice_number,invoice_date,invoice_amount,tax_amount,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (sid,po_id,grn_id,f"INV{n:05d}",id_,ia,ta,ist))
            inv_id = cursor.lastrowid
            if ist=="PAID":
                cursor.execute(
                    "INSERT INTO supplier_payments (invoice_id,payment_amount,payment_date,payment_method,reference_number) VALUES (%s,%s,%s,%s,%s)",
                    (inv_id,ia+ta,id_+timedelta(days=random.randint(5,30)),
                     random.choice(pay_meths),f"REF{random.randint(100000,999999)}"))

    print(f"   ✔  {'purchase cycle (PO+GRN+Invoice+Payment)':45s}  60 POs")

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 5 — INVENTORY
# ══════════════════════════════════════════════════════════════════════════════
def insert_inventory(cursor, prod_map, wh_ids):
    stocks=[]; layers=[]; txns=[]
    for pi in prod_map.values():
        for wid in wh_ids:
            total=0
            for _ in range(random.randint(1,3)):
                bd=rand_date(2023,2024); qr=round(random.uniform(20,200),3)
                qrem=round(qr*random.uniform(0.3,1.0),3); uc=round(pi["pp"]*random.uniform(0.95,1.05),2)
                total+=qrem
                layers.append((pi["id"],wid,None,qr,qrem,uc,bd))
                txns.append((pi["id"],wid,"IN","PO",0,round(qr,3),uc))
            stocks.append((pi["id"],wid,round(total,3)))
    cursor.executemany(
        "INSERT INTO inventory_stock (product_id,warehouse_id,quantity_on_hand) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE quantity_on_hand=VALUES(quantity_on_hand)",
        stocks); print(f"   ✔  {'inventory_stock':45s}  {len(stocks):>5} rows")
    cursor.executemany(
        "INSERT INTO inventory_cost_layers (product_id,warehouse_id,po_item_id,quantity_received,quantity_remaining,unit_cost,received_date) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        layers); print(f"   ✔  {'inventory_cost_layers':45s}  {len(layers):>5} rows")
    cursor.executemany(
        "INSERT INTO inventory_transactions (product_id,warehouse_id,transaction_type,reference_type,reference_id,quantity,unit_cost) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        txns); print(f"   ✔  {'inventory_transactions':45s}  {len(txns):>5} rows")

def insert_stock_adjustments(cursor, prod_map, wh_ids, emp_ids):
    types=["DAMAGE","SHRINKAGE","MANUAL","COUNT"]; skus=list(prod_map.keys())
    data=[]
    for _ in range(30):
        pi=prod_map[random.choice(skus)]; wid=random.choice(wh_ids)
        qb=round(random.uniform(20,150),3); aq=round(random.uniform(-15,10),3)
        data.append((pi["id"],wid,random.choice(types),qb,aq,round(qb+aq,3),fake.sentence(nb_words=6),random.choice(emp_ids)))
    execute_many(cursor,
        "INSERT INTO stock_adjustments (product_id,warehouse_id,adjustment_type,quantity_before,adjusted_qty,quantity_after,reason,adjusted_by) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
        data,"stock_adjustments")

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 6 — TRANSFERS
# ══════════════════════════════════════════════════════════════════════════════
def insert_warehouse_transfers(cursor, prod_map, wh_ids, emp_ids):
    statuses=["COMPLETED","COMPLETED","IN_TRANSIT","PENDING","CANCELLED"]
    skus=list(prod_map.keys())
    for n in range(1,26):
        fw,tw=random.sample(wh_ids,2); td=rand_date(2023,2024)
        st=random.choice(statuses); ca=td+timedelta(days=random.randint(1,5)) if st=="COMPLETED" else None
        cursor.execute(
            "INSERT INTO warehouse_transfers (transfer_number,from_warehouse_id,to_warehouse_id,transfer_date,status,initiated_by,completed_at) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (f"TRF{n:04d}",fw,tw,td,st,random.choice(emp_ids),ca))
        tid=cursor.lastrowid
        for sku in random.sample(skus,k=random.randint(1,4)):
            pi=prod_map[sku]
            cursor.execute(
                "INSERT INTO warehouse_transfer_items (transfer_id,product_id,quantity,unit_cost) VALUES (%s,%s,%s,%s)",
                (tid,pi["id"],round(random.uniform(5,50),3),round(pi["pp"]*random.uniform(0.95,1.02),2)))
    print(f"   ✔  {'warehouse_transfers + items':45s}  25 transfers")

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 7 — POS
# ══════════════════════════════════════════════════════════════════════════════
def insert_pos_sales(cursor, prod_map, store_ids, emp_ids, cust_ids):
    pay_meths=["CASH","CARD","UPI","CASH","UPI"]; skus=list(prod_map.keys())
    for n in range(1,301):
        cid=random.choice(cust_ids) if random.random()>0.35 else None
        sd=rand_date(2023,2024)
        cursor.execute(
            "INSERT INTO pos_sales (bill_number,store_id,cashier_id,customer_id,sale_date,subtotal_amount,discount_amount,tax_amount,total_amount,payment_method) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (f"BILL{n:06d}",random.choice(store_ids),random.choice(emp_ids),cid,sd,0,0,0,0,random.choice(pay_meths)))
        sale_id=cursor.lastrowid; sub=disc=tax=0
        for sku in random.sample(skus,k=random.randint(1,8)):
            pi=prod_map[sku]; qty=round(random.uniform(1,5),3)
            up=round(pi["sp"]*random.uniform(0.97,1.00),2)
            da=round(up*qty*random.uniform(0,0.05),2)
            ta=round((up*qty-da)*0.05,2); tot=round(up*qty-da+ta,2)
            cursor.execute(
                "INSERT INTO pos_sale_items (sale_id,product_id,quantity,unit_price,discount_amount,tax_amount,total_price) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (sale_id,pi["id"],qty,up,da,ta,tot))
            sub+=up*qty; disc+=da; tax+=ta
        cursor.execute(
            "UPDATE pos_sales SET subtotal_amount=%s,discount_amount=%s,tax_amount=%s,total_amount=%s WHERE sale_id=%s",
            (round(sub,2),round(disc,2),round(tax,2),round(sub-disc+tax,2),sale_id))
    print(f"   ✔  {'pos_sales + pos_sale_items':45s}  300 bills")

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    conn   = get_connection()
    cursor = conn.cursor()
    try:
        print("\n─────────────────────────────────────────────────────")
        print("  SECTION 1  ·  Foundation Master Data")
        print("─────────────────────────────────────────────────────")
        uom_map   = insert_units_of_measure(cursor); conn.commit()
        cat_map   = insert_categories(cursor);        conn.commit()
        emp_ids   = insert_employees(cursor);         conn.commit()
        cust_ids  = insert_customers(cursor);         conn.commit()
        sup_ids   = insert_suppliers(cursor);         conn.commit()
        wh_ids    = insert_warehouses(cursor);        conn.commit()
        store_ids = insert_stores(cursor, wh_ids);    conn.commit()
        prod_map  = insert_products(cursor, cat_map, uom_map); conn.commit()

        print("\n─────────────────────────────────────────────────────")
        print("  SECTION 2  ·  GST & Taxation")
        print("─────────────────────────────────────────────────────")
        tax_map = insert_tax_master(cursor); conn.commit()
        insert_product_tax_mapping(cursor, prod_map, tax_map); conn.commit()

        print("\n─────────────────────────────────────────────────────")
        print("  SECTION 3  ·  Reorder & Multi-Source")
        print("─────────────────────────────────────────────────────")
        insert_reorder_rules(cursor, prod_map, wh_ids, sup_ids);         conn.commit()
        insert_supplier_product_rules(cursor, prod_map, sup_ids);        conn.commit()

        print("\n─────────────────────────────────────────────────────")
        print("  SECTION 4  ·  Purchase Cycle  (PO → GRN → Invoice → Payment)")
        print("─────────────────────────────────────────────────────")
        insert_purchase_cycle(cursor, prod_map, wh_ids, sup_ids, emp_ids); conn.commit()

        print("\n─────────────────────────────────────────────────────")
        print("  SECTION 5  ·  Inventory")
        print("─────────────────────────────────────────────────────")
        insert_inventory(cursor, prod_map, wh_ids);                       conn.commit()
        insert_stock_adjustments(cursor, prod_map, wh_ids, emp_ids);      conn.commit()

        print("\n─────────────────────────────────────────────────────")
        print("  SECTION 6  ·  Warehouse Transfers")
        print("─────────────────────────────────────────────────────")
        insert_warehouse_transfers(cursor, prod_map, wh_ids, emp_ids);    conn.commit()

        print("\n─────────────────────────────────────────────────────")
        print("  SECTION 7  ·  POS Billing")
        print("─────────────────────────────────────────────────────")
        insert_pos_sales(cursor, prod_map, store_ids, emp_ids, cust_ids); conn.commit()

        print("\n─────────────────────────────────────────────────────")
        print("  SECTION 8  ·  GST Invoice Details")
        print("─────────────────────────────────────────────────────")
        insert_gst_invoice_details(cursor, tax_map); conn.commit()

        # ── SUMMARY ──────────────────────────────────────────────────────────
        print("\n═════════════════════════════════════════════════════")
        print("  ✅  All data inserted successfully!")
        print("═════════════════════════════════════════════════════")
        tbls = ["units_of_measure","categories","employees","customers","suppliers",
                "warehouses","stores","products","tax_master","product_tax_mapping",
                "gst_invoice_details","inventory_stock","inventory_cost_layers",
                "inventory_transactions","stock_adjustments","purchase_orders",
                "purchase_order_items","goods_receipt_notes","grn_items",
                "supplier_invoices","supplier_payments","pos_sales","pos_sale_items",
                "warehouse_transfers","warehouse_transfer_items",
                "reorder_rules","supplier_product_rules"]
        total = 0
        for t in tbls:
            cursor.execute(f"SELECT COUNT(*) FROM {t}")
            cnt = cursor.fetchone()[0]; total += cnt
            print(f"   {t:45s}  {cnt:>6} rows")
        print(f"   {'─'*45}  {'─'*6}")
        print(f"   {'TOTAL':45s}  {total:>6} rows")
        print("═════════════════════════════════════════════════════\n")

    except Exception as e:
        conn.rollback()
        print(f"\n❌  Error — rolled back: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
        print("🔒  Connection closed.")

if __name__ == "__main__":
    main()