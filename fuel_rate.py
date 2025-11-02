fuel_rates = {
    "Petrol": 72.50,     # Unleaded / Premium Gasoline
    "Diesel": 68.30,                # Common for trucks and public transport
    "CNG": 65.00,
    "LPG": 58.75,         # For taxis and some private cars
    "Electric": 12.00,    # For EVs (approximate cost)
    "Biodiesel": 70.00,        # Diesel with bio component
    "E85": 74.00 # 85% ethanol blend, rare but growing
}
def get_rate(fuel_type):
    return fuel_rates.get(fuel_type, 0)