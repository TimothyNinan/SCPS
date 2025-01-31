from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email, name=None, license_plate=None, credit_card=None, last_entry=None, last_exit=None, password=None, photo=None):
        self.email = email
        self.name = name
        self.license_plate = license_plate
        self.credit_card = credit_card
        self.last_entry = last_entry
        self.last_exit = last_exit
        self.password = password
        self.photo = photo
    
    def get_id(self):
        return self.email

    def to_dict(self):
        """Convert user object to dictionary for Firestore"""
        return {
            'email': self.email,
            'name': self.name,
            'license_plate': self.license_plate, 
            'credit_card': self.credit_card,
            'last_entry': self.last_entry,
            'last_exit': self.last_exit,
            'password': self.password,
            'photo': self.photo
        }

    @staticmethod
    def from_dict(data):
        """Create User object from Firestore dictionary"""
        return User(
            email=data.get('email'),
            name=data.get('name'),
            license_plate=data.get('license_plate'),
            credit_card=data.get('credit_card'),
            last_entry=data.get('last_entry'),
            last_exit=data.get('last_exit'),
            password=data.get('password'),
            photo=data.get('photo')
        )