import re

def get_license_plate(text):
    # List of US state names
    states = {
        'ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA', 'COLORADO',
        'CONNECTICUT', 'DELAWARE', 'FLORIDA', 'GEORGIA', 'HAWAII', 'IDAHO',
        'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS', 'KENTUCKY', 'LOUISIANA',
        'MAINE', 'MARYLAND', 'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA',
        'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA', 'NEVADA',
        'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK',
        'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA', 'OREGON',
        'PENNSYLVANIA', 'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA',
        'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT', 'VIRGINIA', 'WASHINGTON',
        'WEST VIRGINIA', 'WISCONSIN', 'WYOMING'
    }
    
    # Convert text to uppercase
    text = text.upper()
    
    # Split text into words
    words = text.split()
    
    # Pattern for mixed letters and numbers
    pattern = r'^(?=.*[A-Z])(?=.*\d)[A-Z0-9]+$'
    
    # Look for first word containing both letters and numbers that isn't a state
    for word in words:
        # Skip if word is a state name
        if word in states:
            continue
            
        # Check if word matches pattern for mixed letters and numbers
        if re.match(pattern, word):
            return word
                
    return None

