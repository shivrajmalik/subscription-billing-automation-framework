from db_connector import connect_to_db
from UI import shared_data



cust_id=shared_data.customer_id

def get_subscription_by_account(cust_id):
    conn = connect_to_db()
    if not conn:
        print("❌ Failed to connect to DB")
        return None
    else:
        print("✅ Connected to DB")

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tbl_cust WHERE account_no=%s", (cust_id,))
        result = cursor.fetchone()
        print(result)
        shared_data.Customer_data=result
        return result
    finally:
        cursor.close()
        conn.close()

# Example usage
#get_subscription_by_account("cust_id")
