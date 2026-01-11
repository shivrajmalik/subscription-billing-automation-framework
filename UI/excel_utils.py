import openpyxl
from shared_data import *


client_name= client
instance=instance

def get_credentials_for_client_and_instance(client_name, instance, file_path=r"C:path\automation_framework\data\Client_data.xlsx"):
    print("Function Called")
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        header = [cell.value for cell in sheet[1]]
        instance_password_column = f"Password {instance}"
        if instance_password_column not in header:
            return None, None

        password_col_index = header.index(instance_password_column)
        username_col_index = header.index("Username")

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0] and row[0].strip().lower() == client_name.strip().lower():
                username = row[username_col_index]
                password = row[password_col_index]
                print(username,password)
                return username, password
        return None, None
    except Exception as e:
        print(f"Error fetching credentials: {e}")
        return None, None