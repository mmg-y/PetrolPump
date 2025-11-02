fuel_rates = {
    "Petrol": 72.50,
    "Diesel": 68.30,
    "CNG": 65.00,
    "LPG": 58.75,
    "Electric": 12.00,
    "Biodiesel": 70.00,
    "E85": 74.00
}
def get_rate(fuel_type):
    return fuel_rates.get(fuel_type, 0)