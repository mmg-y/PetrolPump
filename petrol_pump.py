import fuel_rate as fr
import datetime
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FUEL_FILE = os.path.join(BASE_DIR, "fuel_transactions.txt")

def menu():
    print("-" * 50)
    print(" Welcome to HP Petrol Pump ".center(50, "-"))
    print("-" * 50)
    print("Available Fuel Types:")
    print("A. Premium Gasoline")
    print("B. Unleaded Gasoline")
    print("C. Diesel")
    print("D. LPG")
    print("V. View Transaction History")
    print("X. Delete Transaction History")
    print("Q. Exit")
    print("-" * 50)

def record_transaction(bill_info):
    with open(FUEL_FILE, "a", encoding="utf-8") as file:
        file.write(bill_info + "\n")

def view_transactions():
    if not os.path.exists(FUEL_FILE):
        print("No transaction history found.")
        return
    print("\n")
    print("-" * 50)
    print("Transaction History" .center(50, "-"))
    print("-" * 50)
    with open(FUEL_FILE, "r", encoding="utf-8") as file:
        for line in file:
            print(line.strip())
    print("-" * 50)

def delete_transactions():
    if os.path.exists(FUEL_FILE):
        os.remove(FUEL_FILE)
        print("Transaction history deleted successfully.")
    else:
        print("No transaction history file to delete.")

def save_bill(bill_no, date_time, fuel_type, quantity, unit, amount, rate, payment_method, amount_paid, change):
    filename = os.path.join(BASE_DIR, f"bill_{bill_no}.txt")
    with open(filename, "w", encoding="utf-8") as file:
        file.write("-" * 50 + "\n")
        file.write("HP Petrol Pump\n" )
        file.write("-" * 50 + "\n")
        file.write(f"Bill No: {bill_no}\n")
        file.write(f"Date & Time: {date_time}\n")
        file.write(f"Fuel Type: {fuel_type}\n")
        file.write(f"Quantity: {quantity:.3f} Liters\n")
        file.write(f"Rate per Liter: ₱{rate:.2f}\n")
        file.write("-" * 50 + "\n")
        file.write(f"Total Amount Due: ₱{amount:.2f}\n")
        file.write(f"Payment Method: {payment_method}\n")

        if payment_method == "Cash":
            file.write(f"Cash Paid: ₱{amount_paid:.2f}\n")
            file.write(f"Change Due: ₱{change:.2f}\n")

        file.write("-" * 50 + "\n")
        file.write("Thank you for your purchase! Visit again.\n")
        file.write("-" * 50 + "\n")


def handle_purchase(fuel_type):
    rate = fr.get_rate(fuel_type)
    if rate == 0:
        print("Error: Could not retrieve fuel rate.")
        return

    print("\n" + "•" * 50)
    print(f"Current Fuel Rate for {fuel_type}: ₱{rate:.2f}/Liter".center(50))
    print("•" * 50)
    print("Mode Selection:")
    print("   1. Fill by Amount (e.g., ₱1,000)")
    print("   2. Fill by Quantity (e.g., 10.0 Liters)")
    print("-" * 50)

    mode_choice = input("   Enter mode (1 or 2): ").strip()

    if mode_choice == '1':
        try:
            amount = float(input(f"   Enter amount to fill (₱): "))
        except ValueError:
            print("   Invalid input. Please enter a number.")
            return

        if amount <= 0:
            print("   Amount must be positive.")
            return
        if amount < rate:
            print(f"   Insufficient amount! Minimum purchase is ₱{rate:.2f} (1 Liter).")
            return
        quantity = amount / rate

    elif mode_choice == '2':
        try:
            quantity = float(input(f"   Enter quantity to fill (Liters): "))
        except ValueError:
            print("   Invalid input. Please enter a number.")
            return

        if quantity <= 0:
            print("   Quantity must be positive.")
            return
        if quantity < 1.0:
            print("   Insufficient quantity! Minimum purchase is 1.0 Liter.")
            return

        amount = round(quantity * rate, 2)

    else:
        print("   Invalid purchase mode selected.")
        return

    print("\n" + "=" * 50)
    print(f"TOTAL BILL: ₱{amount:.2f}")
    print("=" * 50)
    print("Payment Method:")
    print("   A. Cash")
    print("   B. Card (Exact Payment)")

    payment_choice = input("   Enter payment method (A or B): ").upper().strip()

    amount_paid = amount
    change = 0.0
    payment_method = "Card"

    if payment_choice == 'A':
        payment_method = "Cash"
        # Ask how much cash the customer hands over
        try:
            cash_paid = float(input(f"   Enter cash amount paid (₱): "))
        except ValueError:
            print("   Invalid input. Please enter a number.")
            return

        if cash_paid < amount:
            print("   Payment failed! Cash paid is less than the total bill.")
            return

        amount_paid = cash_paid
        change = round(cash_paid - amount, 2)

    elif payment_choice == 'B':
        payment_method = "Card"
        print("   Card payment processed successfully.")
        pass

    else:
        print("   Invalid payment method selected.")
        return

    generate_bill(fuel_type, amount, quantity, rate, payment_method, amount_paid, change)


def generate_bill(fuel_type, amount, quantity, rate, payment_method, amount_paid, change):
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bill_no = random.randint(100000, 999999)

    save_bill(bill_no, date_time, fuel_type, quantity, "Liters", amount, rate, payment_method, amount_paid, change)

    bill_info = f"{bill_no} | {date_time} | {fuel_type} | {quantity:.3f} L | ₱{amount:.2f} | {payment_method}"
    record_transaction(bill_info)

    print("\n")
    print("\n" + "*" * 50)
    print("TRANSACTION COMPLETE".center(50))
    print("*" * 50)
    print(f" Bill No: {bill_no}")
    print(f" Date & Time: {date_time}")
    print("-" * 50)
    print(f" Fuel Type: {fuel_type}")
    print(f" Rate/Liter: ₱{rate:.2f}")
    print(f" Quantity:   {quantity:.3f} Liters")
    print("-" * 50)
    print(f" **TOTAL DUE:** ₱{amount:.2f}")
    print(f" Payment: {payment_method}")

    if payment_method == "Cash":
        print(f" Cash Received: ₱{amount_paid:.2f}")
        if change > 0:
            print(f" **CHANGE DUE:** ₱{change:.2f}")

    print("-" * 50)
    print(" Thank you for your purchase! Visit again. ".center(50))
    print("*" * 50)


def main():
    while True:
        try:
            menu()
            choice = input("Enter your choice: ").upper().strip()

            if choice == 'A':
                fuel_type = "Premium Gasoline"
            elif choice == 'B':
                fuel_type = "Unleaded Gasoline"
            elif choice == 'C':
                fuel_type = "Diesel"
            elif choice == 'D':
                fuel_type = "LPG"
            elif choice == 'V':
                view_transactions()
                continue
            elif choice == 'X':
                delete_transactions()
                continue
            elif choice == 'Q':
                print("Thank you for visiting HP Petrol Pump. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
                continue

            handle_purchase(fuel_type)

        except ValueError:
            print("Please enter a valid numeric input.")
        except Exception as e:
            # Catching unexpected errors gracefully
            print(f"An unexpected error occurred: {e}")
        finally:
            print("\nReturning to main menu...\n")

if __name__ == "__main__":
    main()
