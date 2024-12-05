from gtts import gTTS
from playsound import playsound
import os


carpeta = "audios/"
     
            
def crearAudio(cadena, nombre):
    nombre = carpeta + nombre
    if os.path.exists(nombre):
        os.remove(nombre)
    tts = gTTS(cadena, lang="es")
    tts.save(nombre)
    
    playsound(nombre)

def leerMenu(tipo):
    if tipo == 1:
        crearAudio("El menu en la seccion de desayunos es: huevos, precio", "menu.mp3")
    

