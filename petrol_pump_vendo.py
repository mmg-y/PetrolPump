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
    print("A. Petrol")
    print("B. Diesel")
    print("C. CNG")
    print("V. View Transaction History")
    print("D. Delete Transaction History")
    print("E. Exit")
    print("-" * 50)

def record_transaction(bill_info):
    with open(FUEL_FILE, "a", encoding="utf-8") as file:
        file.write(bill_info + "\n")

def view_transactions():
    if not os.path.exists(FUEL_FILE):
        print("No transaction history found.")
        return
    print("\n=== Transaction History ===")
    with open(FUEL_FILE, "r", encoding="utf-8") as file:
        for line in file:
            print(line.strip())
    print("============================\n")

def delete_transactions():
    if os.path.exists(FUEL_FILE):
        os.remove(FUEL_FILE)
        print("Transaction history deleted successfully.")
    else:
        print("No transaction history file to delete.")

def save_bill_to_file(bill_no, date_time, fuel_type, quantity, unit, amount, rate):
    filename = os.path.join(BASE_DIR, f"bill_{bill_no}.txt")
    with open(filename, "w", encoding="utf-8") as file:
        file.write("-" * 50 + "\n")
        file.write("HP Petrol Pump\n")
        file.write("-" * 50 + "\n")
        file.write(f"Bill No: {bill_no}\n")
        file.write(f"Date & Time: {date_time}\n")
        file.write(f"Fuel Type: {fuel_type}\n")
        file.write(f"Quantity: {round(quantity, 2)} {unit}\n")
        file.write(f"Rate per {unit[:-1]}: ₱{rate}\n")
        file.write(f"Total Amount: ₱{amount}\n")
        file.write("-" * 50 + "\n")
        file.write("Thank you for your purchase! Visit again.\n")
        file.write("-" * 50 + "\n")

def generate_bill(fuel_type, amount):
    rate = fr.get_rate(fuel_type)
    if rate == 0:
        print("Invalid fuel type.")
        return

    unit = "Kg" if fuel_type == "CNG" else "Liters"
    quantity = amount / rate
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bill_no = random.randint(100000, 999999)

    # Save bill file
    save_bill_to_file(bill_no, date_time, fuel_type, quantity, unit, amount, rate)

    # Log transaction in master file
    bill_info = f"{bill_no} | {date_time} | {fuel_type} | {round(quantity,2)} {unit} | ₱{amount}"
    record_transaction(bill_info)

def main():
    while True:
        try:
            menu()
            choice = input("Enter your choice: ").upper().strip()

            if choice == 'A':
                fuel_type = "Petrol"
            elif choice == 'B':
                fuel_type = "Diesel"
            elif choice == 'C':
                fuel_type = "CNG"
            elif choice == 'V':
                view_transactions()
                continue
            elif choice == 'D':
                delete_transactions()
                continue
            elif choice == 'E':
                print("Thank you for visiting HP Petrol Pump. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
                continue

            # Enter amount
            amount = float(input(f"Enter amount for {fuel_type}: "))
            rate = fr.get_rate(fuel_type)

            if amount <= 0:
                print("Amount must be positive.")
                continue
            elif amount < rate:
                print(
                    f"Insufficient amount! Minimum should be at least ₱{rate} for 1 {('Kg' if fuel_type == 'CNG' else 'Liter')}.")
                continue

            generate_bill(fuel_type, amount)

        except ValueError:
            print("Please enter valid numeric input.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            print("\nReturning to main menu...\n")

if __name__ == "__main__":
    main()