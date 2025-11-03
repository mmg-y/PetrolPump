fuel_rates = {
    "Premium Gasoline": 75.00,
    "Unleaded Gasoline": 72.50,
    "Diesel": 68.30,
    "LPG": 58.75

}
def get_rate(fuel_type):
    return fuel_rates.get(fuel_type, 0)