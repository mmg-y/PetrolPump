import fuel_rate as fr
import datetime
import random
import os
import hashlib
import re

total_width = 70  # Set all border widths here
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FUEL_FILE = os.path.join(BASE_DIR, "fuel_transactions.txt")
USER_FILE = os.path.join(BASE_DIR, "users.txt")
CARD_FILE = os.path.join(BASE_DIR, "card_balances.txt")  # File to store card balances

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def validate_password(password):
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def input_password(prompt="Enter password: "):
    import sys, os
    if os.name == 'nt':
        import msvcrt
        print(prompt, end='', flush=True)
        password = ''
        while True:
            ch = msvcrt.getch()
            if ch in {b'\r', b'\n'}:
                print('')
                break
            elif ch == b'\x08':
                if len(password) > 0:
                    password = password[:-1]
                    print('\b \b', end='', flush=True)
            elif ch == b'\x03':
                raise KeyboardInterrupt
            else:
                password += ch.decode('utf-8', errors='ignore')
                print('*', end='', flush=True)
        return password
    else:
        import termios, tty
        print(prompt, end='', flush=True)
        password = ''
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in ('\r', '\n'):
                    print('')
                    break
                elif ch == '\x7f':
                    if len(password) > 0:
                        password = password[:-1]
                        print('\b \b', end='', flush=True)
                else:
                    password += ch
                    print('*', end='', flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return password

# --------------------- CARD SYSTEM FUNCTIONS ---------------------
def get_card_balance(card_number):
    """Retrieve balance for a given card."""
    if not os.path.exists(CARD_FILE):
        return 0.0
    with open(CARD_FILE, "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            parts = line.strip().split(",")
            if len(parts) < 2:
                continue
            card, balance = parts[0], parts[1]
            if card == card_number:
                try:
                    return float(balance)
                except ValueError:
                    return 0.0
    return 0.0

def update_card_balance(card_number, new_balance):
    """Update or add a card's new balance."""
    lines = []
    updated = False

    if os.path.exists(CARD_FILE):
        with open(CARD_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()

    with open(CARD_FILE, "w", encoding="utf-8") as file:
        for line in lines:
            if not line.strip():
                continue
            parts = line.strip().split(",")
            if len(parts) < 2:
                continue
            card = parts[0]
            balance = parts[1]
            if card == card_number:
                file.write(f"{card},{new_balance:.2f}\n")
                updated = True
            else:
                file.write(f"{card},{balance}\n")
        if not updated:
            file.write(f"{card_number},{new_balance:.2f}\n")
# ----------------------------------------------------------------

def login():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * total_width)
        print(" LOGIN ".center(total_width, "-"))
        print("=" * total_width)

        if not os.path.exists(USER_FILE):
            print("Error: 'users.txt' not found!")
            example_hash = hash_password("Admin@1234")
            print(f"Example user line:\nadmin,{example_hash}")
            input("\nPress Enter to exit...")
            exit()

        print("\n")
        username = input("Enter username: ").strip()
        password = input_password("Enter password: ").strip()
        hashed_input = hash_password(password)

        with open(USER_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if "," in line:
                    user, stored_hash = line.strip().split(",", 1)
                    if user == username and stored_hash == hashed_input:
                        print(f"\nLogin successful! Welcome, {username}.\n")
                        input("Press Enter to continue...")
                        return True

        print("\nInvalid username or password. Please try again.\n")
        input("Press Enter to retry...")

def menu():
    print("\n")
    print("=" * total_width)
    print(" WELCOME TO HP PETROL PUMP ".center(total_width, "-"))
    print("=" * total_width)
    print("\nAvailable Options:")
    print(" A. Premium Gasoline")
    print(" B. Unleaded Gasoline")
    print(" C. Diesel")
    print(" D. LPG")
    print(" V. View Transaction History")
    print(" S. View Sales Summary")
    print(" Q. Exit")
    print("\n")
    print("-" * total_width)

def record_transaction(bill_info):
    with open(FUEL_FILE, "a", encoding="utf-8") as file:
        file.write(bill_info + "\n")

def view_transactions():
    if not os.path.exists(FUEL_FILE):
        print("No transaction history found.")
        return

    transactions = []
    with open(FUEL_FILE, "r", encoding="utf-8") as file:
        for line in file:
            parts = [p.strip() for p in line.strip().split("|")]
            if len(parts) < 6:
                continue
            bill_no, date_time, fuel_type, quantity, amount, payment_info = parts
            transactions.append({
                "Bill No": bill_no,
                "Date & Time": date_time,
                "Fuel Type": fuel_type,
                "Quantity": quantity,
                "Amount": amount,
                "Payment Info": payment_info
            })

    headers = ["Bill No", "Date & Time", "Fuel Type", "Quantity", "Amount", "Payment Info"]
    col_widths = {h: len(h) for h in headers}
    for txn in transactions:
        for h in headers:
            col_widths[h] = max(col_widths[h], len(str(txn[h])))

    total_line_width = sum(col_widths.values()) + len(headers) * 3 + 1
    total_line_width = max(total_line_width, total_width)

    print("\n")
    print("\n" + "-" * total_line_width)
    print("TRANSACTION HISTORY".center(total_line_width))
    print("-" * total_line_width)

    header_line = "| " + " | ".join(f"{h:<{col_widths[h]}}" for h in headers) + " |"
    print(header_line)
    print("-" * total_line_width)

    for txn in transactions:
        row = "| " + " | ".join(f"{str(txn[h]):<{col_widths[h]}}" for h in headers) + " |"
        print(row)

    print("-" * total_line_width)
    print("End of Transaction History".center(total_line_width))
    print("-" * total_line_width)

def view_sales():
    if not os.path.exists(FUEL_FILE):
        print("No sales data found.")
        return

    sales = {}
    with open(FUEL_FILE, "r", encoding="utf-8") as file:
        for line in file:
            parts = [p.strip() for p in line.strip().split("|")]
            if len(parts) < 6:
                continue
            _, _, fuel_type, quantity, amount, _ = parts
            try:
                qty_val = float(quantity.replace("L", "").strip())
                amt_val = float(amount.replace("₱", "").strip())
            except ValueError:
                continue
            if fuel_type not in sales:
                sales[fuel_type] = {"Liters": 0, "Amount": 0}
            sales[fuel_type]["Liters"] += qty_val
            sales[fuel_type]["Amount"] += amt_val

    headers = ["Fuel Type", "Total Liters", "Total Sales (₱)"]
    col_widths = {h: len(h) for h in headers}

    for fuel_type, data in sales.items():
        col_widths["Fuel Type"] = max(col_widths["Fuel Type"], len(fuel_type))
        col_widths["Total Liters"] = max(col_widths["Total Liters"], len(f"{data['Liters']:.2f}"))
        col_widths["Total Sales (₱)"] = max(col_widths["Total Sales (₱)"], len(f"{data['Amount']:.2f}"))

    total_line_width = sum(col_widths.values()) + len(headers) * 3 + 1
    total_line_width = max(total_line_width, total_width)

    print("\n" + "-" * total_line_width)
    print("SALES SUMMARY".center(total_line_width))
    print("-" * total_line_width)

    header_line = "| " + " | ".join(f"{h:<{col_widths[h]}}" for h in headers) + " |"
    print(header_line)
    print("-" * total_line_width)

    grand_total = 0
    for fuel_type, data in sales.items():
        row = (
            f"| {fuel_type:<{col_widths['Fuel Type']}} | "
            f"{data['Liters']:<{col_widths['Total Liters']}.2f} | "
            f"{data['Amount']:<{col_widths['Total Sales (₱)']}.2f} |"
        )
        print(row)
        grand_total += data["Amount"]

    print("-" * total_line_width)
    print(f"{'Grand Total Sales:':>{total_line_width - 20}} ₱{grand_total:,.2f}")
    print("-" * total_line_width)

def handle_purchase(fuel_type):
    rate = fr.get_rate(fuel_type)
    if rate == 0:
        print("Error: Could not retrieve fuel rate.")
        return

    print("\n")
    print("\n" + "-" * total_width)
    print(f"Current Fuel Rate for {fuel_type}: ₱{rate:.2f}/Liter".center(total_width))
    print("-" * total_width)
    print("Mode Selection:")
    print("   1. Fill by Amount")
    print("   2. Fill by Quantity")
    print("-" * total_width)

    mode_choice = input("   Enter mode (1 or 2): ").strip()

    if mode_choice == '1':
        amount = float(input("   Enter amount to fill (₱): "))
        if amount <= 0 or amount < rate:
            print("   Invalid or too low amount.")
            return
        quantity = amount / rate
    elif mode_choice == '2':
        quantity = float(input("   Enter quantity to fill (Liters): "))
        if quantity <= 0:
            print("   Invalid quantity.")
            return
        amount = round(quantity * rate, 2)
    else:
        print("   Invalid mode.")
        return

    print("\n")
    print("\n" + "-" * total_width)
    print(f"TOTAL BILL: ₱{amount:.2f}".center(total_width))
    print("-" * total_width)
    print("Payment Method:\n   A. Cash\n   B. Card")
    pay = input("   Enter payment method (A/B): ").upper().strip()
    change = 0
    paid = amount
    method = "Card"
    remaining_balance = None

    if pay == "A":
        method = "Cash"
        paid = float(input("   Enter cash amount: ₱"))
        if paid < amount:
            print("   Payment failed. Not enough cash.")
            return
        change = round(paid - amount, 2)
    elif pay == "B":
        method = "Card"
        card_number = input("   Enter your card number: ").strip()

        # --- Card Deduction Logic (copied exactly) ---
        balance = get_card_balance(card_number)
        if balance <= 0:
            print("   Card not found or has no balance. Please top up.")
            return

        if balance < amount:
            print(f"   Insufficient balance! Card has only ₱{balance:.2f}.")
            return

        new_balance = balance - amount
        update_card_balance(card_number, new_balance)
        remaining_balance = new_balance

        print("\n" + "-" * total_width)
        print(f"   Card Number: {card_number}")
        print(f"   Amount Deducted: ₱{amount:.2f}")
        print(f"   Remaining Balance: ₱{new_balance:.2f}")
        print("-" * total_width)
        # ------------------------------------------------

    else:
        print("Invalid payment option.")
        return

    generate_bill(fuel_type, amount, quantity, rate, method, paid, change, remaining_balance)

def generate_bill(fuel_type, amount, quantity, rate, method, paid, change, remaining_balance=None):
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bill_no = random.randint(100000, 999999)
    save_bill(bill_no, date_time, fuel_type, quantity, "Liters", amount, rate, method, paid, change, remaining_balance)
    # transaction history will keep same format (method only) to match original behavior
    bill_info = f"{bill_no} | {date_time} | {fuel_type} | {quantity:.3f} L | ₱{amount:.2f} | {method}"
    record_transaction(bill_info)

    print("\n")
    print("\n" + "*" * total_width)
    print("TRANSACTION COMPLETE".center(total_width))
    print("*" * total_width)
    print(f"Bill No: {bill_no}")
    print(f"Date & Time: {date_time}")
    print(f"Fuel Type: {fuel_type}")
    print(f"Quantity: {quantity:.3f} Liters @ ₱{rate:.2f}/L")
    print(f"Total Due: ₱{amount:.2f}")
    print(f"Payment: {method}")
    if method == "Cash":
        print(f"Cash Paid: ₱{paid:.2f}")
        if change > 0:
            print(f"Change: ₱{change:.2f}")
    elif method == "Card" and remaining_balance is not None:
        print(f"Amount Deducted: ₱{amount:.2f}")
        print(f"Remaining Card Balance: ₱{remaining_balance:.2f}")
    print("-" * total_width)
    print("Thank you for your purchase!".center(total_width))
    print("*" * total_width)

def save_bill(bill_no, date_time, fuel_type, quantity, unit, amount, rate, method, paid, change, remaining_balance=None):
    filename = os.path.join(BASE_DIR, f"bill_{bill_no}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("-" * total_width + "\n")
        f.write("HP Petrol Pump\n")
        f.write("-" * total_width + "\n")
        f.write(f"Bill No: {bill_no}\n")
        f.write(f"Date & Time: {date_time}\n")
        f.write(f"Fuel Type: {fuel_type}\n")
        f.write(f"Quantity: {quantity:.3f} Liters\n")
        f.write(f"Rate: ₱{rate:.2f}/L\n")
        f.write("-" * total_width + "\n")
        f.write(f"Total: ₱{amount:.2f}\n")
        f.write(f"Payment: {method}\n")
        if method == "Cash":
            f.write(f"Cash Paid: ₱{paid:.2f}\nChange: ₱{change:.2f}\n")
        elif method == "Card" and remaining_balance is not None:
            f.write(f"Amount Deducted: ₱{amount:.2f}\n")
            f.write(f"Remaining Card Balance: ₱{remaining_balance:.2f}\n")
        f.write("-" * total_width + "\nThank you!\n")

def main():
    login()
    while True:
        try:
            menu()
            choice = input("Enter your choice: ").upper().strip()

            if choice == 'A':
                handle_purchase("Premium Gasoline")
            elif choice == 'B':
                handle_purchase("Unleaded Gasoline")
            elif choice == 'C':
                handle_purchase("Diesel")
            elif choice == 'D':
                handle_purchase("LPG")
            elif choice == 'V':
                view_transactions()
            elif choice == 'S':
                view_sales()
            elif choice == 'Q':
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Thank you for visiting HP Petrol Pump. Goodbye!\n")
                break
            else:
                print("Invalid option. Please try again.")
                continue

        except ValueError:
            print("Please enter a valid numeric input.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            print("\nReturning to main menu...\n")

if __name__ == "__main__":
    main()
