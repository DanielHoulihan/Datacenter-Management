import requests

def get_carbon_intensity():
    """Retrives data from CO2 Signal API

    Returns:
        Float: cureent carbon intensity 
        Flaot: fossil fuel percentage
    """
    
    url = "https://api.co2signal.com/v1/latest?countryCode=IE"
    response = requests.get(url,headers={'auth-token': '7E8zL4Ol7wOxNg1LxV9qcKi436eOw3JB'})
    data = response.json()
    return data['data']['carbonIntensity'], data['data']['fossilFuelPercentage']
