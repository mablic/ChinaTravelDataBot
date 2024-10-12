import firebase_admin
from firebase_admin import credentials, firestore, storage
import os

# Firebase configuration
cred = credentials.Certificate("./python-connection.json")
firebase_app = firebase_admin.initialize_app(cred)

# Get Firestore database instance
db = firestore.client()

# Export the Firebase app, Firestore, and Storage instances
__all__ = ['firebase_app', 'db']
