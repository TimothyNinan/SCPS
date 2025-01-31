import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firestore DB
cred = credentials.Certificate('./keys/smart-camera-parking-system-61282fd7a87b.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
database = db.collection('users')

 
def addUser(user):
    """
    Adds a new user to the database.
    """
    doc_ref = database.add(user)
    
def getUserByLicensePlate(license_plate:str) -> dict:
    """
    Gets a user from the database by license plate.
    @param license_plate:str - The license plate of the user
    @return:dict - The user's information if found, None otherwise
    """
    docs = database.where('license_plate', '==', license_plate).get()
    if docs:
        return docs[0].to_dict()
    else:
        return None
    
def getUserByEmail(email:str) -> dict:
    """
    Gets a user from the database by email.
    @param email:str - The email of the user
    @return:dict - The user's information if found, None otherwise
    """
    docs = database.where('email', '==', email).get()
    if docs:
        return docs[0].to_dict()
    else:
        return None

def getUsers():
    """
    Gets all users from the database.
    @return:list - A list of all users in the database
    """
    docs = database.stream()
    users = []
    for doc in docs:
        users.append(doc.to_dict())
    return users

def getMostRecentUser():
    """
    Gets the most recent user from the database.
    @return:dict - The most recent user in the database
    """
    docs = database.order_by('last_entry', direction=firestore.Query.DESCENDING).limit(1).get()
    return docs[0].to_dict()


def updateUser(user):
    """
    Updates a user's information in the database.
    """
    docs = database.where('email', '==', user['email']).get()
    if docs:
        doc_ref = docs[0].reference
        doc_ref.update(user)  
        return doc_ref.id
    else:
        return None

def updateUserByLicensePlate(license_plate:str, user:dict):
    """
    Updates a user's information in the database by license plate.
    """
    docs = database.where('license_plate', '==', license_plate).get()
    if docs:
        doc_ref = docs[0].reference
        doc_ref.update(user)  
        return doc_ref.id

def deleteUser(email:str):
    """
    Deletes a user from the database.
    @param email:str - The email of the user
    """
    doc_ref = database.document(email)
    doc_ref.delete()
    
def deleteAllUsers():
    """
    Deletes all users from the database.
    """
    docs = database.stream()
    for doc in docs:
        doc.reference.delete()

    
    
