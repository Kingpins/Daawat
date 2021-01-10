from gtts import gTTS
import os
from pathlib import Path
from .firebase_service import *

BASE_DIR = Path(__file__).resolve().parent.parent

def HotelIntro(HotelName,Bio):
    text = "Dear Customer, Welcome to " + HotelName +", This hotel is known for "+ Bio +", In order to begin your digital menu experience, Please provide your good name and click Go to menu button, Thank you."
    myobj = gTTS(text=text,lang='en',slow=False,)
    path_of_storage = os.path.join(BASE_DIR,'audioclips')
    myobj.save(path_of_storage+"/"+HotelName+".mp3")
    storage_link = storage.child("hotelAudioClips/"+HotelName+".mp3").put(path_of_storage+"/"+HotelName+".mp3")
    
def HotelCategories(HotelCategories,HotelName):
    text = "The cuisine of our hotel are as follows,"
    for name in HotelCategories:
        text += name + ', '
    text += "Start placing your orders, Enjoy the Daawat! Thank you."
    myobj = gTTS(text=text,lang='en',slow=False,)
    path_of_storage = os.path.join(BASE_DIR,'audioclips')
    myobj.save(path_of_storage+"/"+HotelName+"Categories.mp3")
    storage_link = storage.child("hotelAudioClips/"+HotelName+"Categories.mp3").put(path_of_storage+"/"+HotelName+"Categories.mp3")

def PlaceOrder():
    text = "You can place as many order as you want, until you make your bill in the My Bill section, Thank You"
    myobj = gTTS(text=text,lang='en',slow=False,)
    path_of_storage = os.path.join(BASE_DIR,'audioclips')
    myobj.save(path_of_storage+"/PlaceOrder.mp3")
    storage_link = storage.child("hotelAudioClips/PlaceOrder.mp3").put(path_of_storage+"/PlaceOrder.mp3")
