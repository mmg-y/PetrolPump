fuel_rates = {
    "Petrol": 72.50,   
    "Diesel": 68.30,
    "CNG": 65.00
}
def get_rate(fuel_type):
    return fuel_rates.get(fuel_type, 0)