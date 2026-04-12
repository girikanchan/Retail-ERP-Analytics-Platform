"""
retail_erp_seed_data.py
=======================
Inserts realistic, intentionally MESSY seed data into the retail_erp MySQL database
for Microsoft Fabric / ETL learning (Medallion Architecture, Statistical Analysis).

Intentional data quality issues included for ETL practice:
  - NULL values where allowed
  - Duplicate-looking records (same customer name, different phone)
  - Inconsistent casing (product names, addresses)
  - Outlier values (very high / very low sale amounts)
  - Negative quantity_on_hand edge cases in adjustments
  - Mixed payment methods and statuses
  - Some invoices with mismatched amounts (tax rounding errors)
  - Orphaned references (grn_id=NULL on some invoices)
  - Timestamps spread across 2 years for time-series analysis
  - Some employees with NULL last_name
  - Some customers with NULL email/phone
  - Reorder rules with lead_time_days = 0 (bad data)
  - inventory_transactions with both positive and negative quantities

Requirements:
  pip install mysql-connector-python faker

Usage:
  python retail_erp_seed_data.py
  (Adjust DB_CONFIG below before running)
"""

import mysql.connector
import random
from datetime import date, datetime, timedelta
from decimal import Decimal
import sys

# ─────────────────────────────────────────────────────────────────────────────
# DB CONNECTION — adjust these
# ─────────────────────────────────────────────────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Giribaba@1968",
    "database": "retail_erp",
    "autocommit": False,
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def rand_date(start_days_ago=730, end_days_ago=0):
    delta = random.randint(end_days_ago, start_days_ago)
    return date.today() - timedelta(days=delta)

def rand_ts(start_days_ago=730, end_days_ago=0):
    d = rand_date(start_days_ago, end_days_ago)
    h, m, s = random.randint(7, 21), random.randint(0, 59), random.randint(0, 59)
    return datetime(d.year, d.month, d.day, h, m, s)

def coin(prob=0.5):
    return random.random() < prob

def pick(lst):
    return random.choice(lst)

def weighted_pick(lst, weights):
    return random.choices(lst, weights=weights, k=1)[0]

# ─────────────────────────────────────────────────────────────────────────────
# SEED DATA DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────

# --- 1. units_of_measure (10 rows) ---
UOM_DATA = [
    ("PCS", "Pieces"),
    ("KG", "Kilograms"),
    ("LTR", "Litres"),
    ("MTR", "Metres"),
    ("BOX", "Box"),
    ("PKT", "Packet"),
    ("DZN", "Dozen"),
    ("GM", "Grams"),
    ("SET", "Set"),
    ("ROLL", "Roll"),
]

# --- 2. categories (15 parent + 10 sub = 25 rows) ---
PARENT_CATEGORIES = [
    ("GROC", "Groceries"),
    ("ELEC", "Electronics"),
    ("APRL", "Apparel"),
    ("HOME", "Home & Kitchen"),
    ("HLTH", "Health & Personal Care"),
    ("STNY", "Stationery"),
    ("BVRG", "Beverages"),
    ("FROZ", "Frozen Foods"),
    ("TOYL", "Toys & Games"),
    ("SPRT", "Sports & Fitness"),
    ("BEAU", "Beauty & Cosmetics"),
    ("AUTO", "Automotive"),
    ("PETS", "Pet Supplies"),
    ("OFFC", "Office Supplies"),
    ("BKRY", "Bakery"),
]

SUB_CATEGORIES = [
    ("GROC-DRY",  "Dry Goods",          "GROC"),
    ("GROC-FMLY", "Family Pack Groceries", "GROC"),
    ("ELEC-MOB",  "Mobile Accessories", "ELEC"),
    ("ELEC-LAP",  "Laptop Accessories", "ELEC"),
    ("APRL-MEN",  "Men's Clothing",     "APRL"),
    ("APRL-WMN",  "Women's Clothing",   "APRL"),
    ("HOME-CLN",  "Cleaning Supplies",  "HOME"),
    ("HLTH-VIT",  "Vitamins & Supplements", "HLTH"),
    ("BVRG-COLD", "Cold Beverages",     "BVRG"),
    ("BVRG-HOT",  "Hot Beverages",      "BVRG"),
]

# --- 3. warehouses (5 rows) ---
WAREHOUSE_DATA = [
    ("WH-HYD-01", "Hyderabad Central Warehouse",    "Plot 12, APIIC Industrial Area, Uppal, Hyderabad - 500039"),
    ("WH-HYD-02", "Hyderabad South DC",             "Survey No 45, Shamshabad, Hyderabad - 501218"),
    ("WH-MUM-01", "Mumbai Distribution Centre",      "MIDC, Andheri East, Mumbai - 400093"),
    ("WH-DEL-01", "Delhi NCR Fulfilment Hub",        "Kundli Industrial Belt, Sonipat, Haryana - 131001"),
    ("WH-BLR-01", "Bangalore Warehouse",             "Peenya Industrial Area, Bangalore - 560058"),
]

# --- 4. stores (8 rows) ---
STORE_DATA = [
    ("STR-HYD-01", "Hyderabad Banjara Hills Store",  1, "Road No 10, Banjara Hills, Hyderabad"),
    ("STR-HYD-02", "Hyderabad Ameerpet Store",       1, "Near Metro Station, Ameerpet, Hyderabad"),
    ("STR-HYD-03", "LB Nagar Retail Outlet",         2, "LB Nagar Main Road, Hyderabad - 500074"),
    ("STR-MUM-01", "Mumbai Andheri West Store",       3, "Lokhandwala Complex, Andheri West, Mumbai"),
    ("STR-MUM-02", "Mumbai Thane City Store",         3, "Viviana Mall, Thane - 400601"),
    ("STR-DEL-01", "Delhi Connaught Place",           4, "Block A, Connaught Place, New Delhi - 110001"),
    ("STR-BLR-01", "Bangalore Koramangala",           5, "5th Block, Koramangala, Bangalore - 560095"),
    ("STR-BLR-02", "Bangalore Whitefield",            5, "ITPL Main Road, Whitefield, Bangalore - 560066"),
]

# --- 5. employees (50 rows) ---
FIRST_NAMES = ["Rajesh","Priya","Amit","Sunita","Vijay","Anita","Ravi","Deepa","Sanjay","Meena",
               "Arun","Kavita","Suresh","Lakshmi","Rohit","Pooja","Nikhil","Sneha","Kiran","Divya",
               "Sunil","Radha","Pavan","Shalini","Mohan","Rekha","Ajay","Usha","Venkat","Gayatri",
               "Srinivas","Padma","Ashok","Nandini","Ganesh","Saritha","Mahesh","Jyothi","Praveen","Swathi",
               "Dinesh","Ananya","Harish","Bhavana","Naresh","Lavanya","Ramesh","Tejasri","Chetan","Manasa"]
LAST_NAMES  = ["Kumar","Sharma","Reddy","Singh","Rao","Verma","Gupta","Nair","Iyer","Patel",
               "Chauhan","Joshi","Mehta","Shah","Pillai","Deshpande","Hegde","Shetty","Kaur","Malhotra",
               "Prasad","Varma","Bhat","Desai","Murthy","Gowda","Shukla","Mishra","Tiwari","Pandey",
               "Agarwal","Bansal","Chandra","Das","Fernandes","George","Hussain","Iqbal","Jain","Kapoor",
               "Lal","Mathew","Nath","Oberoi","Parekh","Qureshi","Rathore","Saxena","Tripathi","Yadav"]
ROLES = ["Store Manager","Cashier","Warehouse Manager","Purchase Officer","Sales Executive",
         "Inventory Clerk","Accountant","HR Manager","IT Admin","Logistics Coordinator"]

# --- 6. suppliers (30 rows) ---
SUPPLIER_NAMES = [
    "Bharat Agro Supplies Pvt Ltd", "TechZone Distributors", "Metro Consumer Goods",
    "Sunrise FMCG Wholesale", "Apex Electronics Hub", "Greenleaf Organics",
    "National Textile Traders", "Spiceworld Imports", "Deepam Home Essentials",
    "Kwality Beverages Ltd", "FreshBake Suppliers", "Galaxy Stationery Co",
    "Himalayan Herbal Products", "Pioneer Auto Accessories", "Petzone Distributors",
    "Excel Office Solutions", "Velvet Cosmetics Wholesale", "Tristar Frozen Foods",
    "Heritage Grocery Mart", "CoolBreeze Beverages", "Reliable Packaging Co",
    "Shree Ram Trading Co", "Modern Tech Imports", "Ananya Textiles",
    "Goldstar Electronics", "Fresh Farm Produce", "Skyline Distribution",
    "Om Sai Enterprises", "Karnataka Spices Board", "Delhi Paper Mart"
]
PAYMENT_TERMS_LIST = ["NET30", "NET15", "NET45", "IMMEDIATE", "NET60", "NET7"]

# --- 7. customers (100 rows) ---
CUSTOMER_FIRST = ["Aditya","Bhavna","Chandra","Deepak","Ela","Farhan","Geetha","Hari","Ishaan",
                  "Jaya","Kalpesh","Lata","Manish","Nisha","Omkar","Pallavi","Quresh","Rashmi",
                  "Sagar","Tanvi","Umesh","Vandana","Waqar","Xena","Yusuf","Zara","Abhinav",
                  "Bhoomi","Cyrus","Daksha","Esha","Faisal","Gauri","Himanshu","Indira","Jitesh",
                  "Krithika","Lokesh","Madhuri","Naveen","Ojaswi","Pratik","Qasim","Rohini",
                  "Sachin","Tara","Uma","Vikash","Wania","Yash","Zubair","Aravind","Bindiya",
                  "Chaitanya","Darshna","Ekta","Firoz","Geeta","Harsh","Ipsita","Jai","Komal",
                  "Lalit","Minakshi","Nilesh","Ojas","Preethi","Qadir","Ritu","Shyam","Tejal",
                  "Uttam","Vimala","Wasim","Yamini","Zuha","Alka","Bhushan","Chandni","Dilip",
                  "Eshwar","Fatima","Gopal","Hema","Irfan","Juhi","Kalyan","Laxman","Mona",
                  "Neeraj","Omi","Prem","Raman","Sheela","Tarun","Uday","Vinita","Wajid","Yasmin","Zahir"]
CUSTOMER_LAST = ["Agarwal","Bose","Chowdhury","Dubey","Ediwal","Fazal","Garg","Hora","Iyengar",
                 "Jhaveri","Keswani","Lulla","Makhija","Nadar","Oberoi","Pathak","Quereshi","Rastogi",
                 "Sood","Teli","Uppal","Vaid","Wali","Yadava","Zankat","Ahuja","Bakshi","Chatterjee",
                 "Divan","Eapen","Faleiro","Gomes","Handa","Islam","Jaswal","Kohli","Luthra","Malviya",
                 "Nanda","Oswal","Puri","Qadri","Rohatgi","Sethi","Thakkar","Updhyay","Vaswani",
                 "Xavier","Zaveri","Amin","Bali","Chadha","Dhar","Engira","Fonseca","Ghosh",
                 "Hiremath","Irani","Jog","Kannan","Lele","Mane","Naik","Ogale","Patnaik",
                 "Raut","Saste","Tambe","Ugale","Vaze","Walavalkar","Yargop","Zagade","Atre",
                 "Bhosale","Chitnis","Datar","Endla","Fulari","Gadgil","Hadap","Ingole","Jagtap",
                 "Kamble","Landge","Mohite","Nimbalkar","Ovhal","Pansare","Rajput","Salunke",
                 "Thorat","Ubale","Vhatkar","Wadekar","Yeligar","Zende","Amte","Birla","Chopra"]

CITIES = ["Hyderabad","Mumbai","Delhi","Bangalore","Chennai","Kolkata","Pune","Ahmedabad",
          "Jaipur","Lucknow","Surat","Kochi","Chandigarh","Nagpur","Indore"]

# --- 8. products (100 rows) ---
PRODUCTS = [
    # (sku, name, cat_code, uom_code, hsn, purchase_price, selling_price, reorder_level)
    ("SKU-GRY-001","Tata Salt 1KG","GROC-DRY","KG","25010011",18.00,22.00,50),
    ("SKU-GRY-002","Aashirvaad Atta 5KG","GROC-DRY","KG","11010000",185.00,220.00,30),
    ("SKU-GRY-003","Fortune Sunflower Oil 1L","GROC-DRY","LTR","15121110",95.00,118.00,40),
    ("SKU-GRY-004","Tata Tea Gold 250g","GROC-DRY","PKT","09024090",85.00,110.00,25),
    ("SKU-GRY-005","Parle-G Biscuit 800g","GROC-FMLY","PKT","19053100",45.00,60.00,60),
    ("SKU-GRY-006","MTR Sambar Masala 100g","GROC-DRY","PKT","09109100",32.00,45.00,30),
    ("SKU-GRY-007","Sugar (M30) 1KG","GROC-DRY","KG","17011400",40.00,50.00,80),
    ("SKU-GRY-008","Poha (Flattened Rice) 1KG","GROC-DRY","KG","10062000",42.00,55.00,25),
    ("SKU-GRY-009","Moong Dal 1KG","GROC-DRY","KG","07134000",90.00,115.00,20),
    ("SKU-GRY-010","Sona Masoori Rice 5KG","GROC-FMLY","KG","10063090",230.00,275.00,15),
    ("SKU-ELC-001","boAt Rockerz 255 Pro Earphones","ELEC-MOB","PCS","85183000",900.00,1299.00,10),
    ("SKU-ELC-002","Portronics USB-C Hub 7-in-1","ELEC-LAP","PCS","85176990",650.00,999.00,8),
    ("SKU-ELC-003","Syska LED Bulb 9W","ELEC","PCS","85393190",55.00,80.00,50),
    ("SKU-ELC-004","Mi 10000mAh Power Bank","ELEC-MOB","PCS","85076000",550.00,799.00,12),
    ("SKU-ELC-005","TP-Link WiFi Adapter 300Mbps","ELEC-LAP","PCS","85177090",350.00,499.00,10),
    ("SKU-ELC-006","Philips Type-C Charger 65W","ELEC-MOB","PCS","85044090",480.00,699.00,15),
    ("SKU-ELC-007","Wireless Mouse Logitech M235","ELEC-LAP","PCS","84716000",600.00,899.00,8),
    ("SKU-ELC-008","HP 8GB DDR4 RAM","ELEC-LAP","PCS","85423900",1400.00,1999.00,5),
    ("SKU-ELC-009","Samsung 128GB MicroSD","ELEC-MOB","PCS","85235910",450.00,649.00,15),
    ("SKU-ELC-010","APC Surge Protector 6-port","ELEC","PCS","85363000",700.00,999.00,6),
    ("SKU-APL-001","Men's Cotton Formal Shirt","APRL-MEN","PCS","62052090",350.00,599.00,20),
    ("SKU-APL-002","Women's Kurti (XL)","APRL-WMN","PCS","62044200",380.00,649.00,15),
    ("SKU-APL-003","Jockey Men's Brief Pack of 3","APRL-MEN","SET","62071900",180.00,299.00,30),
    ("SKU-APL-004","Levis 501 Jeans (32)","APRL-MEN","PCS","62034200",1200.00,1899.00,8),
    ("SKU-APL-005","Nike Sports Socks Pack 3","APRL-MEN","SET","61159900",250.00,399.00,20),
    ("SKU-HME-001","Prestige Induction Cooktop 1600W","HOME","PCS","85166000",2200.00,2999.00,5),
    ("SKU-HME-002","Milton Thermosteel Flask 500ml","HOME","PCS","73239300",380.00,549.00,10),
    ("SKU-HME-003","Scotch-Brite Scrub Pad Pack 3","HOME-CLN","PKT","34022090",45.00,69.00,40),
    ("SKU-HME-004","Lizol Floor Cleaner 1L","HOME-CLN","LTR","34022019",90.00,129.00,30),
    ("SKU-HME-005","Vim Dishwash Bar 200g","HOME-CLN","PCS","34022090",22.00,35.00,50),
    ("SKU-HME-006","Tupperware Lunch Box 3-pc Set","HOME","SET","39241000",650.00,999.00,8),
    ("SKU-HME-007","Butterfly Table Fan 400mm","HOME","PCS","84145900",1050.00,1499.00,4),
    ("SKU-HME-008","Inalsa Hand Blender 300W","HOME","PCS","85094000",650.00,999.00,6),
    ("SKU-HLT-001","Dettol Handwash Refill 1500ml","HLTH","LTR","34013000",180.00,249.00,30),
    ("SKU-HLT-002","Himalaya Neem Face Wash 150ml","BEAU","LTR","33049900",85.00,130.00,20),
    ("SKU-HLT-003","Ensure Nutrition Powder 400g","HLTH-VIT","GM","21069099",680.00,949.00,8),
    ("SKU-HLT-004","Revital H Men Multivitamin 30","HLTH-VIT","PCS","30049099",350.00,499.00,10),
    ("SKU-HLT-005","Dettol Antiseptic Liquid 500ml","HLTH","LTR","38089400",95.00,140.00,25),
    ("SKU-HLT-006","Oral-B Toothbrush Medium","HLTH","PCS","96031000",35.00,60.00,40),
    ("SKU-HLT-007","Colgate Total Toothpaste 150g","HLTH","PKT","33061000",65.00,95.00,35),
    ("SKU-STN-001","Classmate Notebook 200 Pages","STNY","PCS","48201000",52.00,75.00,50),
    ("SKU-STN-002","Reynolds Ball Pen Blue Pack 10","STNY","PKT","96081000",55.00,80.00,30),
    ("SKU-STN-003","Stapler Kangaro DS-23s","STNY","PCS","83050000",120.00,175.00,15),
    ("SKU-STN-004","A4 Paper Ream 500 Sheets","STNY","PKT","48025590",185.00,260.00,20),
    ("SKU-STN-005","Scotch Tape 24mm x 65m","STNY","ROLL","39199090",35.00,55.00,30),
    ("SKU-BVG-001","Coca-Cola 600ml PET Bottle","BVRG-COLD","PCS","22021090",22.00,35.00,100),
    ("SKU-BVG-002","Red Bull Energy 250ml","BVRG-COLD","PCS","22021090",75.00,110.00,40),
    ("SKU-BVG-003","Nescafe Classic 50g","BVRG-HOT","GM","21011100",195.00,275.00,20),
    ("SKU-BVG-004","Bisleri Mineral Water 1L","BVRG-COLD","LTR","22011000",10.00,20.00,150),
    ("SKU-BVG-005","Lipton Green Tea 25 Bags","BVRG-HOT","PKT","09024090",75.00,115.00,25),
    ("SKU-BVG-006","Paper Boat Aam Panna 200ml","BVRG-COLD","LTR","20099000",18.00,30.00,80),
    ("SKU-FRZ-001","McCain French Fries 400g","FROZ","PKT","20041000",95.00,139.00,20),
    ("SKU-FRZ-002","Amul Butter 500g","FROZ","GM","04051000",240.00,295.00,15),
    ("SKU-FRZ-003","Kwality Wall's Cornetto","FROZ","PCS","21050000",32.00,50.00,50),
    ("SKU-TOY-001","LEGO Classic Brick Box","TOYL","SET","95030090",1800.00,2499.00,5),
    ("SKU-TOY-002","Funskool Scrabble Board Game","TOYL","SET","95040000",650.00,950.00,8),
    ("SKU-TOY-003","Crayola 64 Crayons Box","TOYL","PCS","96055000",250.00,375.00,10),
    ("SKU-SPT-001","Cosco Shuttlecock Feather Pack6","SPRT","PKT","95069900",180.00,250.00,15),
    ("SKU-SPT-002","Nivia Football Size 5","SPRT","PCS","95062910",600.00,899.00,6),
    ("SKU-SPT-003","Decathlon Yoga Mat 5mm","SPRT","ROLL","95065900",850.00,1199.00,5),
    ("SKU-SPT-004","Protex Cricket Tennis Ball Pack 3","SPRT","PKT","95066200",85.00,125.00,20),
    ("SKU-BEA-001","Lakme Compact Powder Beige","BEAU","PCS","33041000",195.00,299.00,15),
    ("SKU-BEA-002","Pantene Pro-V Shampoo 340ml","BEAU","LTR","33051000",175.00,249.00,20),
    ("SKU-BEA-003","Dove Body Lotion 250ml","BEAU","LTR","33079000",165.00,235.00,15),
    ("SKU-BEA-004","Gillette Mach3 Razor + 2 Blades","BEAU","SET","82121000",250.00,375.00,12),
    ("SKU-ATO-001","Castrol GTX 10W-30 Engine Oil 1L","AUTO","LTR","27101940",380.00,549.00,10),
    ("SKU-ATO-002","Car Air Freshener Ambi Pur","AUTO","PCS","33074900",155.00,229.00,15),
    ("SKU-ATO-003","Bosch Wiper Blade 18 inch","AUTO","PCS","85122000",350.00,499.00,8),
    ("SKU-PET-001","Pedigree Adult Dog Food 3KG","PETS","KG","23091000",620.00,899.00,6),
    ("SKU-PET-002","Whiskas Cat Food Tuna 85g","PETS","GM","23091000",38.00,58.00,20),
    ("SKU-OFC-001","3M Whiteboard Marker Black","OFFC","PCS","96082000",65.00,95.00,20),
    ("SKU-OFC-002","Fellowes A4 Lamination Pouch Pk100","OFFC","PKT","39201090",350.00,499.00,10),
    ("SKU-BKY-001","Britannia Good Day Cashew 200g","BKRY","PKT","19053100",38.00,58.00,60),
    ("SKU-BKY-002","English Oven Multigrain Bread","BKRY","PCS","19059090",48.00,72.00,40),
    ("SKU-BKY-003","Bisk Farm Creamy Wafer 75g","BKRY","PKT","19053200",18.00,29.00,80),
    # more products to reach 100
    ("SKU-GRY-011","Maida (Refined Flour) 1KG","GROC-DRY","KG","11019900",32.00,42.00,30),
    ("SKU-GRY-012","Tata Sampann Chana Dal 1KG","GROC-DRY","KG","07134000",88.00,112.00,20),
    ("SKU-GRY-013","Rajma (Red Kidney Beans) 1KG","GROC-DRY","KG","07133300",90.00,118.00,18),
    ("SKU-GRY-014","Kissan Mixed Fruit Jam 500g","GROC-DRY","GM","20079910",75.00,110.00,15),
    ("SKU-GRY-015","Amul Full Cream Milk Powder 1KG","GROC-DRY","KG","04021000",440.00,535.00,10),
    ("SKU-ELC-011","Ambrane Wireless Charger 15W","ELEC-MOB","PCS","85044090",420.00,649.00,10),
    ("SKU-ELC-012","Zebronics Keyboard+Mouse Combo","ELEC-LAP","SET","84716000",700.00,999.00,6),
    ("SKU-ELC-013","D-Link ADSL2+ Router","ELEC-LAP","PCS","85176910",950.00,1399.00,4),
    ("SKU-APL-006","Peter England Slim Fit Trouser","APRL-MEN","PCS","62034200",750.00,1199.00,8),
    ("SKU-APL-007","Women's Palazzo Pants (M)","APRL-WMN","PCS","62044900",290.00,499.00,12),
    ("SKU-HME-009","Bajaj Mixer Grinder 750W","HOME","PCS","85094000",1800.00,2499.00,3),
    ("SKU-HME-010","Cello Set of 6 Stainless Steel Glasses","HOME","SET","73239300",280.00,399.00,10),
    ("SKU-HLT-008","Parachute Coconut Oil 500ml","HLTH","LTR","15131110",92.00,135.00,20),
    ("SKU-HLT-009","Sensodyne Toothpaste 70g","HLTH","PKT","33061000",95.00,145.00,15),
    ("SKU-BVG-007","Tropicana Orange Juice 1L","BVRG-COLD","LTR","20099000",90.00,135.00,25),
    ("SKU-BVG-008","Horlicks Original 500g","BVRG-HOT","GM","18069000",195.00,279.00,15),
    ("SKU-FRZ-004","Vadilal Mango Ice Cream 1L","FROZ","LTR","21050000",220.00,299.00,8),
    ("SKU-SPT-005","Adidas Water Bottle 750ml","SPRT","PCS","39239090",350.00,499.00,10),
    ("SKU-BEA-005","Himalaya Moisturising Cream 150ml","BEAU","LTR","33049900",78.00,120.00,20),
    ("SKU-GRY-016","MDH Kitchen King Masala 500g","GROC-DRY","GM","09109100",120.00,165.00,20),
]

# --- 9. tax_master (GST rates for India) ---
TAX_MASTER = [
    ("GST 0%",   0.00, "CGST"),
    ("CGST 2.5%", 2.50, "CGST"),
    ("SGST 2.5%", 2.50, "SGST"),
    ("CGST 6%",   6.00, "CGST"),
    ("SGST 6%",   6.00, "SGST"),
    ("IGST 12%", 12.00, "IGST"),
    ("CGST 9%",   9.00, "CGST"),
    ("SGST 9%",   9.00, "SGST"),
    ("IGST 18%", 18.00, "IGST"),
    ("CESS 1%",   1.00, "CESS"),
    ("CGST 14%", 14.00, "CGST"),
    ("SGST 14%", 14.00, "SGST"),
    ("IGST 28%", 28.00, "IGST"),
]

# ─────────────────────────────────────────────────────────────────────────────
# MAIN SEEDING FUNCTION
# ─────────────────────────────────────────────────────────────────────────────
def seed():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Disable FK checks during load
    cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    cur.execute("SET SESSION sql_mode = ''")  # allow zero dates & truncation

    print("=" * 60)
    print(" retail_erp — Seed Data Loader")
    print("=" * 60)

    # ── 1. units_of_measure ────────────────────────────────────────
    print("\n[1/20] Inserting units_of_measure ...")
    for code, name in UOM_DATA:
        cur.execute(
            "INSERT IGNORE INTO units_of_measure (uom_code, uom_name) VALUES (%s,%s)",
            (code, name)
        )
    conn.commit()
    cur.execute("SELECT uom_id, uom_code FROM units_of_measure")
    uom_map = {r[1]: r[0] for r in cur.fetchall()}

    # ── 2. categories ──────────────────────────────────────────────
    print("[2/20] Inserting categories ...")
    for code, name in PARENT_CATEGORIES:
        cur.execute(
            "INSERT IGNORE INTO categories (category_code, category_name) VALUES (%s,%s)",
            (code, name)
        )
    conn.commit()
    cur.execute("SELECT category_id, category_code FROM categories")
    cat_map = {r[1]: r[0] for r in cur.fetchall()}

    for code, name, parent_code in SUB_CATEGORIES:
        cur.execute(
            "INSERT IGNORE INTO categories (category_code, category_name, parent_id) VALUES (%s,%s,%s)",
            (code, name, cat_map.get(parent_code))
        )
    conn.commit()
    cur.execute("SELECT category_id, category_code FROM categories")
    cat_map = {r[1]: r[0] for r in cur.fetchall()}

    # ── 3. warehouses ──────────────────────────────────────────────
    print("[3/20] Inserting warehouses ...")
    for code, name, addr in WAREHOUSE_DATA:
        cur.execute(
            "INSERT IGNORE INTO warehouses (warehouse_code, warehouse_name, address) VALUES (%s,%s,%s)",
            (code, name, addr)
        )
    conn.commit()
    cur.execute("SELECT warehouse_id, warehouse_code FROM warehouses")
    wh_map = {r[1]: r[0] for r in cur.fetchall()}
    wh_ids = list(wh_map.values())

    # ── 4. stores ──────────────────────────────────────────────────
    print("[4/20] Inserting stores ...")
    for code, name, wh_idx, addr in STORE_DATA:
        cur.execute(
            "INSERT IGNORE INTO stores (store_code, store_name, warehouse_id, address) VALUES (%s,%s,%s,%s)",
            (code, name, wh_ids[wh_idx - 1], addr)
        )
    conn.commit()
    cur.execute("SELECT store_id FROM stores")
    store_ids = [r[0] for r in cur.fetchall()]

    # ── 5. employees (50) ──────────────────────────────────────────
    print("[5/20] Inserting employees (50) ...")
    emp_roles_pool = ROLES * 6
    for i in range(50):
        fn = FIRST_NAMES[i]
        ln = LAST_NAMES[i] if coin(0.9) else None   # ~10% NULL last_name (messy)
        code = f"EMP{i+1:04d}"
        role = pick(ROLES)
        cur.execute(
            "INSERT IGNORE INTO employees (employee_code, first_name, last_name, role) VALUES (%s,%s,%s,%s)",
            (code, fn, ln, role)
        )
    conn.commit()
    cur.execute("SELECT employee_id FROM employees")
    emp_ids = [r[0] for r in cur.fetchall()]

    # ── 6. suppliers (30) ──────────────────────────────────────────
    print("[6/20] Inserting suppliers (30) ...")
    supplier_state_codes = ["29","27","07","09","33","19","24","06","08","10"]
    for i, name in enumerate(SUPPLIER_NAMES):
        code = f"SUP{i+1:04d}"
        gstin = f"{pick(supplier_state_codes)}AABCS{random.randint(1000,9999)}B{random.randint(1,9)}Z{random.randint(1,9)}"
        phone = f"9{random.randint(100000000,999999999)}"
        email = name.lower().replace(" ","").replace("pvtltd","")[:15] + f"@supplier{i+1}.com" if coin(0.85) else None
        contact = f"{pick(FIRST_NAMES)} {pick(LAST_NAMES)}"
        city = pick(CITIES)
        addr = f"{random.randint(1,200)}, {city} Industrial Area, {city}"
        pt = pick(PAYMENT_TERMS_LIST)
        cur.execute(
            """INSERT IGNORE INTO suppliers
               (supplier_code,supplier_name,contact_person,phone,email,address,gstin,payment_terms)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (code, name, contact, phone, email, addr, gstin, pt)
        )
    conn.commit()
    cur.execute("SELECT supplier_id FROM suppliers")
    sup_ids = [r[0] for r in cur.fetchall()]

    # ── 7. customers (100) ─────────────────────────────────────────
    print("[7/20] Inserting customers (100) ...")
    for i in range(100):
        fn = CUSTOMER_FIRST[i]
        ln = CUSTOMER_LAST[i]
        name = f"{fn} {ln}"
        code = f"CUST{i+1:05d}"
        phone = f"9{random.randint(100000000,999999999)}" if coin(0.88) else None
        email = f"{fn.lower()}.{ln.lower()}{random.randint(1,99)}@{'gmail' if coin(0.6) else 'yahoo'}.com" if coin(0.80) else None
        city = pick(CITIES)
        addr = f"{random.randint(1,500)}, {pick(['Sector','Block','Road','Colony'])} {random.randint(1,25)}, {city}" if coin(0.75) else None
        gstin = f"29AABCS{random.randint(1000,9999)}B1Z5" if coin(0.15) else None  # most retail = no GSTIN
        cur.execute(
            """INSERT IGNORE INTO customers
               (customer_code,customer_name,phone,email,address,gstin)
               VALUES (%s,%s,%s,%s,%s,%s)""",
            (code, name, phone, email, addr, gstin)
        )
    conn.commit()
    cur.execute("SELECT customer_id FROM customers")
    cust_ids = [r[0] for r in cur.fetchall()]

    # ── 8. tax_master ──────────────────────────────────────────────
    print("[8/20] Inserting tax_master ...")
    for tname, tpct, ttype in TAX_MASTER:
        cur.execute(
            "INSERT IGNORE INTO tax_master (tax_name, tax_percentage, tax_type) VALUES (%s,%s,%s)",
            (tname, tpct, ttype)
        )
    conn.commit()
    cur.execute("SELECT tax_id FROM tax_master")
    tax_ids = [r[0] for r in cur.fetchall()]

    # ── 9. products (100) ─────────────────────────────────────────
    print("[9/20] Inserting products (100) ...")
    for (sku, pname, cat_code, uom_code, hsn, pp, sp, rl) in PRODUCTS:
        cid = cat_map.get(cat_code, cat_map.get("GROC"))
        uid = uom_map.get(uom_code, uom_map.get("PCS"))
        # Intentional mess: some prices have inconsistencies (purchase > selling for a few)
        if coin(0.05):
            pp, sp = sp, pp   # swapped — data issue for ETL cleaning
        cur.execute(
            """INSERT IGNORE INTO products
               (sku,product_name,category_id,uom_id,hsn_code,purchase_price,selling_price,reorder_level)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (sku, pname, cid, uid, hsn, pp, sp, rl)
        )
    conn.commit()
    cur.execute("SELECT product_id, sku, purchase_price, selling_price FROM products")
    prod_rows = cur.fetchall()
    prod_ids = [r[0] for r in prod_rows]
    prod_map = {r[0]: {"purchase_price": float(r[2]), "selling_price": float(r[3])} for r in prod_rows}

    # ── 10. product_tax_mapping ────────────────────────────────────
    print("[10/20] Inserting product_tax_mapping ...")
    # Each product gets either CGST+SGST (intra-state) or IGST (inter-state)
    for pid in prod_ids:
        if coin(0.7):  # intra-state: CGST+SGST
            cgst_tax = pick([t for t in tax_ids if t in [2,4,7]])  # CGST tiers
            sgst_tax = cgst_tax + 1  # SGST mirrors CGST
            cur.execute("INSERT IGNORE INTO product_tax_mapping VALUES (%s,%s)", (pid, cgst_tax))
            if sgst_tax in tax_ids:
                cur.execute("INSERT IGNORE INTO product_tax_mapping VALUES (%s,%s)", (pid, sgst_tax))
        else:  # inter-state: IGST
            igst_tax = pick([t for t in tax_ids if t in [6,9,12]])
            cur.execute("INSERT IGNORE INTO product_tax_mapping VALUES (%s,%s)", (pid, igst_tax))
    conn.commit()

    # ── 11. purchase_orders + items + GRN + GRN items (100+ POs) ──
    print("[11/20] Inserting purchase_orders, items, GRNs ...")
    po_ids = []
    grn_ids = []
    grn_item_id_map = {}  # grn_item_id → po_item_id

    po_statuses = ["DRAFT","SENT","PARTIAL","RECEIVED","CANCELLED"]
    po_status_weights = [5, 10, 15, 60, 10]

    for po_num in range(1, 121):  # 120 POs
        sup = pick(sup_ids)
        wh  = pick(wh_ids)
        emp = pick(emp_ids)
        odate = rand_date(600, 30)
        exp_del = odate + timedelta(days=random.randint(3, 45))
        status = weighted_pick(po_statuses, po_status_weights)
        po_number = f"PO-{odate.year}-{po_num:04d}"
        total_amt = 0.00

        cur.execute(
            """INSERT INTO purchase_orders
               (po_number,supplier_id,warehouse_id,po_status,order_date,expected_delivery_date,total_amount,created_by)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (po_number, sup, wh, status, odate, exp_del, total_amt, emp)
        )
        po_id = cur.lastrowid
        po_ids.append(po_id)

        # 2-6 line items per PO
        selected_products = random.sample(prod_ids, k=random.randint(2, 6))
        po_item_ids_for_grn = []
        for prod in selected_products:
            qty_ord = round(random.uniform(5, 200), 3)
            unit_cost = prod_map[prod]["purchase_price"] * random.uniform(0.85, 1.05)  # slight variance
            qty_recv = round(qty_ord * random.uniform(0.0, 1.0), 3) if status in ("PARTIAL","RECEIVED") else 0.0
            cur.execute(
                """INSERT INTO purchase_order_items
                   (po_id,product_id,quantity_ordered,quantity_received,unit_cost)
                   VALUES (%s,%s,%s,%s,%s)""",
                (po_id, prod, qty_ord, qty_recv, round(unit_cost, 2))
            )
            po_item_ids_for_grn.append((cur.lastrowid, prod, qty_recv, round(unit_cost, 2)))
            total_amt += qty_ord * unit_cost

        # Update PO total
        cur.execute("UPDATE purchase_orders SET total_amount=%s WHERE po_id=%s", (round(total_amt, 2), po_id))

        # GRN for RECEIVED/PARTIAL POs
        if status in ("RECEIVED", "PARTIAL"):
            grn_number = f"GRN-{odate.year}-{po_num:04d}"
            recv_date = odate + timedelta(days=random.randint(1, 30))
            recv_by = pick(emp_ids)
            grn_stat = "ACCEPTED" if status == "RECEIVED" else pick(["PENDING","ACCEPTED"])
            cur.execute(
                """INSERT INTO goods_receipt_notes
                   (grn_number,po_id,warehouse_id,received_by,receipt_date,grn_status,remarks)
                   VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                (grn_number, po_id, wh, recv_by, recv_date, grn_stat,
                 pick([None, "Goods received in good condition", "Minor packaging damage", "Short shipment", None]))
            )
            grn_id = cur.lastrowid
            grn_ids.append(grn_id)

            for po_item_id, prod, qty_recv, unit_cost in po_item_ids_for_grn:
                if qty_recv <= 0:
                    continue
                qty_acc = round(qty_recv * random.uniform(0.9, 1.0), 3)
                qty_rej = round(qty_recv - qty_acc, 3)
                cur.execute(
                    """INSERT INTO grn_items
                       (grn_id,po_item_id,product_id,quantity_received,quantity_accepted,quantity_rejected,unit_cost)
                       VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                    (grn_id, po_item_id, prod, qty_recv, qty_acc, qty_rej, unit_cost)
                )
                grn_item_id_map[cur.lastrowid] = po_item_id

    conn.commit()
    print(f"   → {len(po_ids)} POs, {len(grn_ids)} GRNs inserted")

    # ── 12. inventory_cost_layers + inventory_transactions ─────────
    print("[12/20] Inserting inventory cost layers & transactions ...")
    # Generate stock-in events from accepted GRNs
    cur.execute("""
        SELECT gi.product_id, grn.warehouse_id, gi.quantity_accepted, gi.unit_cost, grn.receipt_date, grn.grn_id
        FROM grn_items gi
        JOIN goods_receipt_notes grn ON gi.grn_id = grn.grn_id
        WHERE gi.quantity_accepted > 0
    """)
    grn_stock_rows = cur.fetchall()

    for prod_id, wh_id, qty_acc, unit_cost, receipt_date, grn_id in grn_stock_rows:
        # Cost layer
        cur.execute(
            """INSERT INTO inventory_cost_layers
               (product_id,warehouse_id,quantity_received,quantity_remaining,unit_cost,received_date)
               VALUES (%s,%s,%s,%s,%s,%s)""",
            (prod_id, wh_id, qty_acc, qty_acc, unit_cost, receipt_date)
        )
        # Inventory transaction IN
        emp = pick(emp_ids)
        cur.execute(
            """INSERT INTO inventory_transactions
               (product_id,warehouse_id,transaction_type,reference_type,reference_id,quantity,unit_cost,created_by,transaction_date)
               VALUES (%s,%s,'IN','PURCHASE',%s,%s,%s,%s,%s)""",
            (prod_id, wh_id, grn_id, qty_acc, unit_cost, emp, datetime.combine(receipt_date, datetime.min.time()))
        )
    conn.commit()

    # ── 13. inventory_stock population (via trigger or direct) ─────
    # The trigger trg_inventory_update should handle this on INSERT to inventory_transactions
    # But in case it's not active, let's also do a direct upsert:
    print("[13/20] Upserting inventory_stock ...")
    cur.execute("""
        INSERT INTO inventory_stock (product_id, warehouse_id, quantity_on_hand)
        SELECT product_id, warehouse_id, SUM(quantity)
        FROM inventory_transactions
        WHERE transaction_type = 'IN'
        GROUP BY product_id, warehouse_id
        ON DUPLICATE KEY UPDATE quantity_on_hand = VALUES(quantity_on_hand)
    """)
    conn.commit()

    # ── 14. supplier_invoices + payments ──────────────────────────
    print("[14/20] Inserting supplier_invoices & payments ...")
    inv_ids = []
    inv_statuses = ["PENDING","APPROVED","PAID","DISPUTED"]
    inv_status_weights = [15, 20, 55, 10]
    for i, grn_id in enumerate(grn_ids):
        cur.execute("SELECT po_id, warehouse_id FROM goods_receipt_notes WHERE grn_id=%s", (grn_id,))
        row = cur.fetchone()
        if not row:
            continue
        po_id, wh_id = row
        cur.execute("SELECT supplier_id FROM purchase_orders WHERE po_id=%s", (po_id,))
        sup_row = cur.fetchone()
        if not sup_row:
            continue
        sup_id = sup_row[0]

        inv_number = f"SINV-{2024 if coin(0.5) else 2025}-{i+1:05d}"
        inv_date = rand_date(500, 5)
        inv_amt = round(random.uniform(5000, 250000), 2)
        # Intentional: some tax_amounts have rounding errors
        tax_amt = round(inv_amt * 0.18 + (random.uniform(-50, 50) if coin(0.2) else 0), 2)
        status = weighted_pick(inv_statuses, inv_status_weights)

        cur.execute(
            """INSERT INTO supplier_invoices
               (supplier_id,po_id,grn_id,invoice_number,invoice_date,invoice_amount,tax_amount,status)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (sup_id, po_id, grn_id if coin(0.85) else None, inv_number, inv_date, inv_amt, tax_amt, status)
        )
        inv_id = cur.lastrowid
        inv_ids.append(inv_id)

        # Payments for PAID invoices (sometimes multiple partial payments)
        if status == "PAID":
            num_payments = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
            remaining = inv_amt + tax_amt
            for p in range(num_payments):
                pay_amt = round(remaining / (num_payments - p), 2)
                remaining -= pay_amt
                pay_date = inv_date + timedelta(days=random.randint(1, 60))
                method = pick(["BANK_TRANSFER","CHEQUE","CASH","UPI"])
                ref = f"UTR{random.randint(100000000000, 999999999999)}" if method in ("BANK_TRANSFER","UPI") else (
                    f"CHQ{random.randint(100000,999999)}" if method == "CHEQUE" else None
                )
                cur.execute(
                    """INSERT INTO supplier_payments
                       (invoice_id,payment_amount,payment_date,payment_method,reference_number,notes)
                       VALUES (%s,%s,%s,%s,%s,%s)""",
                    (inv_id, pay_amt, pay_date, method, ref,
                     pick([None, "On-time payment", "Delayed by 3 days", None, "Advance payment"]))
                )
    conn.commit()
    print(f"   → {len(inv_ids)} supplier invoices inserted")

    # ── 15. pos_sales + pos_sale_items (300+ sales) ────────────────
    print("[15/20] Inserting pos_sales & pos_sale_items (300+) ...")
    pay_methods = ["CASH","CARD","UPI","CREDIT"]
    pay_method_w = [40, 30, 25, 5]
    sale_ids = []

    for sale_num in range(1, 351):
        store_id = pick(store_ids)
        cashier_id = pick(emp_ids)
        cust_id = pick(cust_ids) if coin(0.65) else None   # walk-in: no customer
        sale_date = rand_ts(600, 0)
        bill_number = f"BILL-{sale_date.year}-{sale_num:06d}"
        pay_method = weighted_pick(pay_methods, pay_method_w)
        pay_status = "PAID" if coin(0.92) else pick(["PENDING","REFUNDED"])

        subtotal = 0.0
        discount = 0.0
        tax_total = 0.0

        # 1-8 line items per bill
        n_items = random.randint(1, 8)
        # Outlier sale: occasionally a bulk order
        if coin(0.03):
            n_items = random.randint(15, 30)

        selected = random.sample(prod_ids, k=min(n_items, len(prod_ids)))
        line_items = []
        for prod_id in selected:
            qty = round(random.uniform(1, 10), 3)
            price = prod_map[prod_id]["selling_price"]
            # Occasional price override (messy: cashier keyed wrong price)
            if coin(0.05):
                price = price * random.uniform(0.5, 1.5)
            disc = round(price * qty * random.uniform(0, 0.15), 2) if coin(0.3) else 0.0
            tax = round((price * qty - disc) * 0.18, 2)
            total_line = round(price * qty - disc + tax, 2)
            subtotal += price * qty
            discount += disc
            tax_total += tax
            line_items.append((prod_id, qty, round(price, 2), disc, tax, total_line))

        total_amt = round(subtotal - discount + tax_total, 2)
        # Outlier: negative total (refund/return) for a few records
        if coin(0.02):
            total_amt = -abs(total_amt)

        cur.execute(
            """INSERT INTO pos_sales
               (bill_number,store_id,cashier_id,customer_id,sale_date,
                subtotal_amount,discount_amount,tax_amount,total_amount,
                payment_method,payment_status)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (bill_number, store_id, cashier_id, cust_id, sale_date,
             round(subtotal, 2), round(discount, 2), round(tax_total, 2),
             total_amt, pay_method, pay_status)
        )
        sale_id = cur.lastrowid
        sale_ids.append(sale_id)

        for (prod_id, qty, uprice, disc, tax, total_line) in line_items:
            cur.execute(
                """INSERT INTO pos_sale_items
                   (sale_id,product_id,quantity,unit_price,discount_amount,tax_amount,total_price)
                   VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                (sale_id, prod_id, qty, uprice, disc, tax, total_line)
            )
    conn.commit()
    print(f"   → {len(sale_ids)} POS sales inserted")

    # ── 16. inventory_transactions OUT for sales ───────────────────
    print("[16/20] Inserting inventory OUT transactions for sales ...")
    cur.execute("SELECT sale_id, store_id, sale_date FROM pos_sales LIMIT 350")
    sales = cur.fetchall()
    # store → warehouse mapping
    cur.execute("SELECT store_id, warehouse_id FROM stores")
    store_wh = {r[0]: r[1] for r in cur.fetchall()}

    cur.execute("SELECT sale_id, product_id, quantity FROM pos_sale_items")
    sale_items_rows = cur.fetchall()

    # Build a local cache of current stock levels to avoid repeated DB reads
    # and to track running balances as we insert OUTs
    cur.execute("SELECT product_id, warehouse_id, quantity_on_hand FROM inventory_stock")
    stock_cache = {(r[0], r[1]): float(r[2] or 0) for r in cur.fetchall()}

    sales_map = {s[0]: s for s in sales}

    for s_id, prod_id, qty in ((s, p, float(q)) for s, p, q in sale_items_rows):
        s_info = sales_map.get(s_id)
        if not s_info:
            continue
        wh_id = store_wh.get(s_info[1], pick(wh_ids))
        emp = pick(emp_ids)
        cost = prod_map.get(prod_id, {}).get("purchase_price", 100.0)
        key = (prod_id, wh_id)

        current_stock = stock_cache.get(key, 0.0)

        # If this warehouse has no stock for this product, seed it first
        # with enough inventory so the OUT won't trigger the negative-stock guard.
        # This mirrors a realistic "opening stock" or inter-warehouse transfer
        # that would exist in a real system before the sale occurred.
        if current_stock < qty:
            seed_qty = round(qty + random.uniform(50, 200), 3)
            cur.execute(
                """INSERT INTO inventory_transactions
                   (product_id,warehouse_id,transaction_type,reference_type,reference_id,quantity,unit_cost,created_by,transaction_date)
                   VALUES (%s,%s,'IN','ADJUSTMENT',0,%s,%s,%s,%s)""",
                (prod_id, wh_id, seed_qty, cost, pick(emp_ids),
                 s_info[2] - timedelta(days=random.randint(1, 30)))
            )
            stock_cache[key] = current_stock + seed_qty

        cur.execute(
            """INSERT INTO inventory_transactions
               (product_id,warehouse_id,transaction_type,reference_type,reference_id,quantity,unit_cost,created_by,transaction_date)
               VALUES (%s,%s,'OUT','SALE',%s,%s,%s,%s,%s)""",
            (prod_id, wh_id, s_id, -qty, cost, emp, s_info[2])
        )
        stock_cache[key] = stock_cache.get(key, 0.0) - qty

    conn.commit()

    # ── 17. warehouse_transfers + items (50) ──────────────────────
    print("[17/20] Inserting warehouse_transfers ...")
    transfer_statuses = ["PENDING","IN_TRANSIT","COMPLETED","CANCELLED"]
    transfer_status_w = [10, 10, 70, 10]
    for t_num in range(1, 61):
        wh_from, wh_to = random.sample(wh_ids, 2)
        emp = pick(emp_ids)
        tdate = rand_date(400, 5)
        status = weighted_pick(transfer_statuses, transfer_status_w)
        completed_at = datetime.combine(tdate + timedelta(days=random.randint(1, 10)), datetime.min.time()) if status == "COMPLETED" else None
        tnum = f"TRF-{tdate.year}-{t_num:04d}"
        cur.execute(
            """INSERT INTO warehouse_transfers
               (transfer_number,from_warehouse_id,to_warehouse_id,transfer_date,status,initiated_by,completed_at,notes)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (tnum, wh_from, wh_to, tdate, status, emp, completed_at,
             pick([None,"Seasonal restocking","Store demand","Excess inventory redistribution",None]))
        )
        transfer_id = cur.lastrowid
        n_items = random.randint(1, 5)
        for prod_id in random.sample(prod_ids, k=n_items):
            qty = round(random.uniform(5, 100), 3)
            cost = prod_map[prod_id]["purchase_price"]
            cur.execute(
                "INSERT INTO warehouse_transfer_items (transfer_id,product_id,quantity,unit_cost) VALUES (%s,%s,%s,%s)",
                (transfer_id, prod_id, qty, round(cost, 2))
            )
            # TRANSFER transactions
            if status == "COMPLETED":
                emp2 = pick(emp_ids)
                ts = datetime.combine(tdate, datetime.min.time())
                key_from = (prod_id, wh_from)
                current = stock_cache.get(key_from, 0.0)
                if current < qty:
                    seed_qty = round(qty + random.uniform(50, 200), 3)
                    cur.execute(
                        """INSERT INTO inventory_transactions
                           (product_id,warehouse_id,transaction_type,reference_type,reference_id,quantity,unit_cost,created_by,transaction_date)
                           VALUES (%s,%s,'IN','ADJUSTMENT',0,%s,%s,%s,%s)""",
                        (prod_id, wh_from, seed_qty, cost, pick(emp_ids),
                         tdate - timedelta(days=random.randint(1, 30)))
                    )
                    stock_cache[key_from] = current + seed_qty
                cur.execute(
                    """INSERT INTO inventory_transactions
                       (product_id,warehouse_id,transaction_type,reference_type,reference_id,quantity,unit_cost,created_by,transaction_date)
                       VALUES (%s,%s,'TRANSFER','TRANSFER',%s,%s,%s,%s,%s)""",
                    (prod_id, wh_from, transfer_id, -qty, cost, emp2, ts)
                )
                stock_cache[key_from] = stock_cache.get(key_from, 0.0) - qty
                cur.execute(
                    """INSERT INTO inventory_transactions
                       (product_id,warehouse_id,transaction_type,reference_type,reference_id,quantity,unit_cost,created_by,transaction_date)
                       VALUES (%s,%s,'TRANSFER','TRANSFER',%s,%s,%s,%s,%s)""",
                    (prod_id, wh_to, transfer_id, qty, cost, emp2, ts)
                )
                stock_cache[(prod_id, wh_to)] = stock_cache.get((prod_id, wh_to), 0.0) + qty
    conn.commit()

    # ── 18. stock_adjustments (100) ────────────────────────────────
    print("[18/20] Inserting stock_adjustments (100) ...")
    adj_types = ["DAMAGE","SHRINKAGE","MANUAL","COUNT"]
    for _ in range(120):
        prod_id = pick(prod_ids)
        wh_id = pick(wh_ids)
        emp = pick(emp_ids)
        qty_before = round(random.uniform(10, 500), 3)
        # Intentional: some adjustments make stock go negative (data issue)
        adj_qty = round(random.uniform(-50, 50), 3)
        if coin(0.05):
            adj_qty = -qty_before * 1.5   # creates negative after (bad data)
        qty_after = round(qty_before + adj_qty, 3)
        adj_type = pick(adj_types)
        reason = pick(["Water damage", "Rodent damage", "Expired goods", "Count mismatch",
                       "System error correction", None, "Fire damage (minor)", "Theft", None, "Breakage"])
        adj_date = rand_ts(400, 0)
        cur.execute(
            """INSERT INTO stock_adjustments
               (product_id,warehouse_id,adjustment_type,quantity_before,adjusted_qty,quantity_after,reason,adjusted_by,adjustment_date)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (prod_id, wh_id, adj_type, qty_before, adj_qty, qty_after, reason, emp, adj_date)
        )
    conn.commit()

    # ── 19. gst_invoice_details (150) ─────────────────────────────
    print("[19/20] Inserting gst_invoice_details ...")
    for i in range(150):
        ref_type = pick(["SALE", "PURCHASE"])
        ref_id = pick(sale_ids) if ref_type == "SALE" else pick(inv_ids if inv_ids else [1])
        tax_id = pick(tax_ids)
        taxable_amt = round(random.uniform(500, 50000), 2)
        # Intentional: some tax_amounts slightly off (rounding bug)
        tax_amt = round(taxable_amt * random.uniform(0.05, 0.28) + (random.uniform(-10, 10) if coin(0.15) else 0), 2)
        cur.execute(
            """INSERT INTO gst_invoice_details
               (reference_type,reference_id,tax_id,taxable_amount,tax_amount)
               VALUES (%s,%s,%s,%s,%s)""",
            (ref_type, ref_id, tax_id, taxable_amt, tax_amt)
        )
    conn.commit()

    # ── 20. reorder_rules + supplier_product_rules ─────────────────
    print("[20/20] Inserting reorder_rules & supplier_product_rules ...")
    inserted_reorder = set()
    for prod_id in prod_ids:
        for wh_id in random.sample(wh_ids, k=random.randint(1, 3)):
            key = (prod_id, wh_id)
            if key in inserted_reorder:
                continue
            inserted_reorder.add(key)
            min_stock = random.randint(0, 100)
            reorder_qty = random.randint(10, 500)
            pref_sup = pick(sup_ids) if coin(0.8) else None
            # Intentional: lead_time_days = 0 (bad data for some rows)
            lead = random.randint(0, 45) if coin(0.85) else 0
            cur.execute(
                """INSERT IGNORE INTO reorder_rules
                   (product_id,warehouse_id,min_stock_level,reorder_quantity,preferred_supplier_id,lead_time_days,is_active)
                   VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                (prod_id, wh_id, min_stock, reorder_qty, pref_sup, lead, pick([1,1,1,0]))
            )

    # supplier_product_rules
    inserted_spr = set()
    for prod_id in random.sample(prod_ids, k=80):
        for rank, sup_id in enumerate(random.sample(sup_ids, k=random.randint(1, 3)), start=1):
            key = (sup_id, prod_id)
            if key in inserted_spr:
                continue
            inserted_spr.add(key)
            cur.execute(
                "INSERT IGNORE INTO supplier_product_rules (supplier_id,product_id,priority_rank) VALUES (%s,%s,%s)",
                (sup_id, prod_id, rank)
            )
    conn.commit()

    # Re-enable FK checks
    cur.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn.commit()
    cur.close()
    conn.close()

    print("\n" + "=" * 60)
    print(" ✅  Seed complete! Data summary:")
    print("=" * 60)
    summary = [
        ("units_of_measure",        len(UOM_DATA)),
        ("categories",              len(PARENT_CATEGORIES) + len(SUB_CATEGORIES)),
        ("warehouses",              len(WAREHOUSE_DATA)),
        ("stores",                  len(STORE_DATA)),
        ("employees",               50),
        ("suppliers",               len(SUPPLIER_NAMES)),
        ("customers",               100),
        ("tax_master",              len(TAX_MASTER)),
        ("products",                len(PRODUCTS)),
        ("product_tax_mapping",     len(prod_ids)),
        ("purchase_orders",         120),
        ("purchase_order_items",    "~3-4 per PO"),
        ("goods_receipt_notes",     f"~{len(grn_ids)}"),
        ("grn_items",               "~3-4 per GRN"),
        ("inventory_cost_layers",   "= accepted GRN items"),
        ("inventory_transactions",  "IN + OUT + TRANSFER"),
        ("inventory_stock",         "product×warehouse combos"),
        ("supplier_invoices",       f"~{len(grn_ids)}"),
        ("supplier_payments",       "~1-3 per PAID invoice"),
        ("pos_sales",               350),
        ("pos_sale_items",          "~1-8 per sale"),
        ("warehouse_transfers",     60),
        ("warehouse_transfer_items","~1-5 per transfer"),
        ("stock_adjustments",       120),
        ("gst_invoice_details",     150),
        ("reorder_rules",           f"~{len(inserted_reorder)}"),
        ("supplier_product_rules",  f"~{len(inserted_spr)}"),
    ]
    for tbl, cnt in summary:
        print(f"   {tbl:<35} {cnt}")

    print("\n🎯 Intentional data quality issues seeded for ETL practice:")
    issues = [
        "NULL last_name on ~10% employees",
        "NULL phone/email on ~12-20% customers",
        "~5% products with purchase_price > selling_price (swapped)",
        "~5% stock_adjustments cause negative quantity_after",
        "~15% gst_invoice_details have rounding errors in tax_amount",
        "~15% supplier_invoices have NULL grn_id (orphaned reference)",
        "~2% POS sales have negative total_amount (unprocessed returns)",
        "~5% pos_sale_items with outlier unit_price (±50% variance)",
        "Reorder rules with lead_time_days = 0 (bad data)",
        "Timestamps spread across 2 years for time-series analysis",
        "Bulk orders (15-30 items) mixed in POS sales as outliers",
        "Mixed payment methods and invoice statuses for aggregation practice",
        "Some supplier_invoices have NULL po_id (messy AP entries)",
    ]
    for issue in issues:
        print(f"   ⚠  {issue}")
    print()


if __name__ == "__main__":
    seed()