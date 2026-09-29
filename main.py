import hashlib
import string
import random
from database import connect_to_database


# ENCRYPT AND VERIFY PIN
def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def verify_pin(input_pin, stored_hash):
    return hash_pin(input_pin) == stored_hash


# DB AND TABLES INITIALIZE
def initialize_tables():
    connection = connect_to_database()
    if not connection:
        return False

    try:
        cursor = connection.cursor()

        create_accounts_table = """
            CREATE TABLE IF NOT EXISTS accounts (
            account_number VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            pin VARCHAR(64) NOT NULL,
            balance DECIMAL(15,2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """

        create_audit_table = """
            CREATE TABLE IF NOT EXISTS audit (
            id SERIAL PRIMARY KEY,
            account_number VARCHAR(50),
            holder_name VARCHAR(100),
            action VARCHAR(100) NOT NULL,
            amount DECIMAL(15,2) DEFAULT 0.00,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_number) REFERENCES accounts(account_number)
            ON DELETE CASCADE
        );
    """

        cursor.execute(create_accounts_table)
        cursor.execute(create_audit_table)

        connection.commit()
        cursor.close()
        return True

    except Exception as error:
        print(f"Error initializing tables: {error}")
        return False


# ACCOUNT CLASS
class Account:
    def __init__(self, name="", pin="", account_number=""):
        self.__account_number = (
            account_number if account_number else self.generate_account_number()
        )
        self.__name = name
        self.__pin = hash_pin(pin) if pin else ""
        self.__balance = 0.0

    @staticmethod
    def generate_account_number():
        return "".join(random.choices(string.ascii_uppercase+string.digits,k=10))

    # GETTERS
    def get_account_number(self):
        return self.__account_number

    def get_name(self):
            return self.__name

    def get_pinhash(self):
            return self.__pin

    def get_balance(self):
            return self.__balance


    # SETTERS
    def set_name(self, name):
        self.__name  = name
    
    def set_pinhash(self, pin):
        self.__pin = hash_pin(pin)
    
    def set_balance(self, balance):
        self.__balance = balance


    # UTILITY
    def deposit(self, amount):
        if amount <= 0:
            return False
        self.__balance += amount
        return True

    def withdraw(self, amount):
        if amount <= 0 or amount > self.__balance:
            return False
        self.__balance -= amount
        return True


    # DATABASE CRUD
    @classmethod
    def load_from_db(cls, account_number, pin):
        connection = connect_to_database()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT account_number,name,pin,balance FROM accounts WHERE account_number=%s",(account_number,)
            )
            result = cursor.fetchone()
            connection.commit()
            cursor.close()
            if result:
                stored_pin_hash = result[2]
                if verify_pin(pin, stored_pin_hash):
                    account = cls(result[1],result[2],result[0])
                    account.set_balance(float(result[3]))
                    account.__pin = stored_pin_hash
                    return account
            return None                

        except Exception as error:
            print(f"ERROR IN LOADING ACCOUNT,{error}")
            return None


    def save_to_db(self):
        connection = connect_to_database()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO accounts (account_number,name,pin,balance)
                VALUES(%s,%s,%s,%s)
                ON CONFLICT (account_number)
                DO UPDATE SET name=%s, pin=%s, balance=%s 
                """,

                (
                    self.__account_number,
                    self.__name,
                    self.__pin,
                    self.__balance,
                    self.__name,
                    self.__pin,
                    self.__balance,
                ),
            )

            connection.commit()
            cursor.close()
            return True
    
        except Exception as error:
            print(f"ERROR IN SAVING ACCOUNT,{error}")
            return None 

    
    def delete_from_db(self):
        connection = connect_to_database()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM audit WHERE account_number=%s",(self.__account_number,),)
            cursor.execute(
                "DELETE FROM accounts WHERE account_number=%s",
                (self.__account_number,),
            )

            connection.commit()
            cursor.close()
            return True
    
        except Exception as error:
            print(f"ERROR IN CLOSING ACCOUNT,{error}")
            return False



# AUDIT CLASS
class Audit:
    @staticmethod
    def log_action(account_number, holder_name, action, amount=0.0):
        connection = connect_to_database()
        if not connection:
            return False

        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO audit (account_number, holder_name, action, amount) VALUES (%s,%s,%s,%s)",
                (  
                    account_number,
                    holder_name,
                    action,
                    amount
                ),
            )
            
            connection.commit()
            cursor.close()
            return True
        
        except Exception as error:
                print(f"ERROR IN AUDITING ACTION,{error}")
                return None


    @staticmethod
    def get_single_audit_logs(account_number):
        connection = connect_to_database()
        if not connection:
            return []

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, holder_name,action,amount, timestamp FROM audit
                WHERE account_number =%s
                ORDER BY timestamp DESC
                """,
                (account_number,),
            )
            results = cursor.fetchall()            
            connection.commit()
            cursor.close()
            logs =[]

            for row in results:
                logs.append(
                    {
                        "id":row[0],
                        "holder_name":row[1],
                        "action":row[2],
                        "amount":row[3],
                        "timestamp":row[4]
                    }
                )
            return logs
        
        except Exception as error:
            return None
            print(f"ERROR IN LOGGING {account_number} ACTIONS,{error}")


    @staticmethod
    def get_all_audit_logs(account_number):
        connection = connect_to_database()
        if not connection:
            return []

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, holder_name,action,amount, timestamp FROM audit
                ORDER BY timestamp DESC
                """
            )
            results = cursor.fetchall()            
            connection.commit()
            cursor.close()
            logs =[]

            for row in results:
                logs.append(
                    {
                        "id":row[0],
                        "holder_name":row[1],
                        "action":row[2],
                        "amount":row[3],
                        "timestamp":row[4]
                    }
                )
            return logs
        
        except Exception as error:
            print(f"ERROR IN LOGGING ALL ACTIONS,{error}")
            return None


    @staticmethod
    def clear_single_audit_logs(account_number):
        connection = connect_to_database()
        if not connection:
            return False

        try:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM audit WHERE account_number =%s ",
                (account_number,),
            )
            connection.commit()
            cursor.close()
            return True
        
        except Exception as error:
                print(f"ERROR IN CLEARING {account_number} ACTIONS,{error}")
                return False


    @staticmethod
    def clear_all_audit_logs(account_number):
        connection = connect_to_database()
        if not connection:
            return False

        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM audit")
            connection.commit()
            cursor.close()
            return True
        
        except Exception as error:
                print(f"ERROR IN CLEARING ALL ACTIONS,{error}")
                return False



# BANKSYSTEM CLASS
class BankSystem:
    def __init__(self):
        initialize_tables()


    def create_account(self, name, pin):
        account = Account(name,pin)

        if account.save_to_db():
            Audit.log_action(account.get_account_number(), account.get_name(), "Account Created", 0.0)
            return account
        return None


    def read_account(self, account_number, pin):
        account = Account.load_from_db(account_number,pin)

        if account:
            Audit.log_action(account_number, account.get_name(),"Details Checked", 0.0)
            return account
        return None


    def update_account(self,account):
        return account.save_to_db()


    def delete_account(self, account_number, pin):
        account = Account.load_from_db(account_number, pin)

        if account:
            success = account.delete_from_db()
            if success:
                Audit.log_action(account_number, account.get_name(), "Account Deleted", 0.0)
                return True
        return False


    def deposit(self, account_number, pin,amount):
        account = Account.load_from_db(account_number,pin)
        if account and account.deposit(amount):
            if account.save_to_db():
                Audit.log_action(account_number, account.get_name(),"Amount Deposited", amount)
                return True
        return False


    def withdraw(self, account_number, pin,amount):
        account = Account.load_from_db(account_number,pin)
        if account and account.withdraw(amount):
            if account.save_to_db():
                Audit.log_action(account_number, account.get_name(),"Amount withdraw", amount)
                return True
        return False


    def get_account_balance(self, account_number, pin):
        account = Account.load_from_db(account_number,pin)
        if account.save_to_db():        
            if account :
                Audit.log_action(account_number, account.get_name(),"Balance Checked",0.0)
                return account.get_balance()
        return None


    def get_single_audit_logs(self, account_number):
        return Audit.get_single_audit_logs(account_number)


    def get_all_audit_logs(self):
        return Audit.get_all_audit_logs()


    def clear_single_audit_logs(self, account_number):
        return Audit.clear_single_audit_logs(account_number)


    def clear_all_audit_logs(self):
        return Audit.clear_all_audit_logs()



# VALID AMOUNT INPUT
def get_valid_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("Amount must be greater than Zero.")
                continue
            return amount
        except ValueError:
            print("Please! Enter a valid amount in numbers.")




# ============================== CLI FUNCTIONS ==============================


# CREATE ACCOUNT CLI
def create_account_cli(bank):
    print("=" * 40)
    print("CREATE NEW ACCOUNT")
    print("=" * 40)

    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty/ignored.")
        input("Press enter to continue...")
        return

    pin = input("Enter 4-digit PIN: ").strip()
    if len(pin) != 4 or not pin.isdigit():
        print("PIN must be 4-digit number.")
        input("Press enter to continue...")
        return

    confirm_pin = input("Confirm your PIN: ").strip()
    if pin != confirm_pin:
        print("PIN is not matching.")
        input("Press enter to continue...")
        return

    account = bank.create_account(name, pin)
    if account:
        print(f"\nAccount successfully created!")
        print(f"Account Number: {account.get_account_number()}")
        print(f"Save your ACCOUNT NUMBER and PIN securely.")
    else:
        print(f"\nAccount cannot be created, try again")
    input("Press enter to continue...")


# LOGGED IN FUNCTIONS
def check_balance_cli(bank,account,pin):
    print("=" * 40)
    print("CURRENT ACCOUNT BALANCE")
    print("=" * 40)

    balance = bank.get_account_balance(account.get_account_number(), pin)
    if balance is not None:
        print(f"Current balance: ₹{balance:.2f}")
    else:
        print("Error checking  balance, try again.")
    input("Press enter to continue...")


def deposit_money_cli(bank,account, pin):
    print("=" * 40)
    print("DEPOSIT MONEY")
    print("=" * 40)
    amount = get_valid_amount("Enter deposit amount:₹ ")
    
    if bank.deposit(account.get_account_number(), pin, amount):
        print(f"₹{amount:.2f} Successfully Deposited")
        balance = bank.get_account_balance(account.get_account_number(), pin)

    if balance is not None:
        print(f"New balance: ₹{balance:.2f}")
    else:
        print("Error in depositing balance, try again.")
    input("Press enter to continue...")


def withdraw_money_cli(bank,account, pin):
    print("=" * 40)
    print("WITHDRAW MONEY")
    print("=" * 40)
    amount = get_valid_amount("Enter withdraw money:₹ ")
    if bank.withdraw(account.get_account_number(), pin, amount):
        print(f"₹{amount:.2f} Successfully withdrawn")
        balance = bank.get_account_balance(account.get_account_number(), pin)

    if balance is not None:
        print(f"New balance: ₹{balance:.2f}")
    else:
        print("Error in withdrawing balance, try again.")
    input("Press enter to continue...")


def view_transaction_history_cli(bank,account, pin):
    print("=" * 40)
    print("USER TRANSACTION HISTORY")
    print("=" * 40)
    logs = bank.get_single_audit_logs(account.get_account_number())
    if not logs:
        print("No Transaction History.")
    else:
        for log in logs:
            print(f"{log['timestamp']} {log['action']} - ₹{log['amount']:.2f} BY {log['holder_name']}")
    input("Press enter to continue...")


def update_account_info_cli(bank,account, pin):
    print("=" * 40)
    print("UPDATE ACCOUNT INFO")
    print("=" * 40)

    new_name = input("Enter your new_name: ").strip()
    if new_name:
        account.set_name(new_name)
        if bank.update_account(account):
            Audit.log_action(account.get_account_number(), account.get_name(), "Account Name Updated", 0.00)
            print("Name Updated Successfully")
        else:
            print("Error in Updating Account")
    else:
        print("No Changes Occur.")
    input("Press enter to continue...")


def change_pin_logout_cli(bank,account, pin):
    print("=" * 40)
    print("CHANGE ACCOUNT PIN")
    print("=" * 40)

    old_pin = input("Enter Old PIN: ").strip()
    if old_pin != pin:
        print("Incorrect Current PIN")
        input("Press enter to continue...")
        return False

    new_pin = input("Enter 4-digit new_pin: ").strip()

    if len(new_pin) != 4 or not new_pin.isdigit():
        print("PIN must be 4-digit number.")
        input("Press enter to continue...")
        return

    confirm_pin = input("Confirm your PIN: ").strip()
    if new_pin != confirm_pin:
        print("PIN is not matching.")
        input("Press enter to continue...")
        return False

    account.set_pinhash(new_pin)
    if bank.update_account(account):
        Audit.log_action(account.get_account_number(), account.get_name(), "PIN Changed Auto Logout", 0.00)
        print("PIN Updated Successfully. You will be logged out.")
        print("Press Enter to Continue...")
        return True

    print("Error in Updating PIN")
    print("Press Enter to Continue...")
    return False


def delete_account_cli(bank, account, pin):
    print("=" * 40)
    print("CLOSE ACCOUNT")
    print("=" * 40)

    comfirm = input("Are you sure, you want to delete this account? (yes/no): ").strip().lower()
    if comfirm != "yes":
        print("Account Deletion Cancelled.")
        input("Press enter to continue...")
        return False

    re_pin = input("Re-Enter your PIN to confirm: ").strip()

    if re_pin != pin:
        print("PIN did not match. Account not Closed")
        input("Press enter to continue...")
        return False

    if bank.delete_account(account.get_account_number(),pin):
        print("Account Closed Successfully.")
        input("Press enter to continue...")
        return True

    print("Error in Closing Account, try again...")
    print("Press Enter to Continue...")
    return False



# LOGIN ACCOUNT CLI
def login_account_cli(bank):
    print("=" * 40)
    print("LOGIN ACCOUNT")
    print("=" * 40)

    account_number = input("Enter your Account Number: ").strip()
    if not account_number:
        print("Account Number cannot be empty/ignored.")
        input("Press enter to continue...")
        return

    pin = input("Enter 4-digit PIN: ").strip()
    account = bank.read_account(account_number, pin)
    if not account:
        print("Wrong Credientials.")
        input("Press enter to continue...")
        return

    while True:
        print("=" * 40)
        print(f"WELCOME, {account.get_name()}!")
        print(f"ACCOUNT NUMBER: {account.get_account_number()}")
        print("=" * 40)
        print("1. Check Balance")
        print("2. Deposit Amount")
        print("3. Withdraw Amount")
        print("4. Transaction History")
        print("5. Update Account Info")
        print("6. Update PIN")
        print("7. Close Account")
        print("8. Logout")
        print("=" * 40)
        
        choice = input("Enter your choice(1-7): ").strip()
        
        if choice == "1":
            check_balance_cli(bank,account, pin)
        elif choice == "2":
            deposit_money_cli(bank,account, pin)
        elif choice == "3":
            withdraw_money_cli(bank,account, pin)
        elif choice == "4":
            view_transaction_history_cli(bank,account, pin)
        elif choice == "5":
            update_account_info_cli(bank,account, pin)
        elif choice == "6":
            if change_pin_logout_cli(bank, account, pin):
                break
        elif choice == "7":
            if delete_account_cli(bank, account, pin):
                break
        elif choice == "8":
            break
        else:
            print("Inavlid Choice, Please try again.")
            input("Press enter to continue...")



# MAIN MENU OF CLI
def main_menu_cli():
    bank = BankSystem()


    while True:
        print("=" * 40)
        print("-------- BANK MANAGEMENT SYSTEM --------")
        print("=" * 40)
        print("1. New Account")
        print("2. Login Account")
        # print("="*13, "ADMINS ONLY","="*13)
        # print("3. View All Audit Logs")
        # print("4. View Single Audit Logs")
        # print("5. Clear All Audit Logs")
        # print("6. Clear Single Audit Logs")
        print("5. Exit")
        print("=" * 40)

        choice = input("Enter your choice(1-5): ").strip()

        if choice == "1":
            create_account_cli(bank)
        elif choice == "2":
            login_account_cli(bank)
        elif choice == "5":
            print("Thankyou so much For using our services, do visit again!")
            break
        else:
            print("Inavlid Choice, Please try again.")
            input("Press enter to continue...")


if __name__ == "__main__":
    main_menu_cli()