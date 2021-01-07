import pyrebase
# configuration for firebase storage and database
config = {
    "apiKey": "AIzaSyCi5-vfmk7VW2xFtgacj3_arjL04KeaW2A",
    "authDomain": "dawaat-9e0f1.firebaseapp.com",
    "databaseURL":"https://dawaat-9e0f1-default-rtdb.firebaseio.com",
    "projectId": "dawaat-9e0f1",
    "storageBucket": "dawaat-9e0f1.appspot.com",
    "messagingSenderId": "55134356040",
    "appId": "1:55134356040:web:ea4f51040695d9d59f0e7d",
    "measurementId": "G-Z2N8MPTMYK"
};

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
