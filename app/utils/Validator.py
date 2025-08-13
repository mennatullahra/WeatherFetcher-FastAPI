import re

class Validator:
    
    def validate_city_name(self, city: str) -> bool:
        if not city.strip():
            return False
        if re.search(r'[^a-zA-Z\s]', city):
            return False
        return True
