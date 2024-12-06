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
    playsound("audios/timbre.mp3")
    playsound(nombre)
    playsound("audios/timbre.mp3")
    

def leerMenu(tipo):
    if tipo == 1:
        crearAudio("""
                   El menú en la sección de Bebidas es: Bebida 1: cocaCola. Descripción: refresco de 355 mililitros. el precio es de: 26 pesos.
                   Bebida 2: Piña Colada. Descripción: bebida de 355 mililitros con jugo de piña y crema de coco con alcohol y hielos. el precio es de 125 pesos.""", "menu.mp3")
    if tipo == 2:
        crearAudio("""
                   El menú en la sección de Pescados es: Platillo 1, Mojarra frita. Descripción: aproximadamente un peso de 450 a 500 gramos, se sirve con arroz y ensalada. El precio del platillo es de 145 pesos.
                    Platillo 2, filete empanizado. 
                    Descripción: aproximadamente un peso de 450 a 500 gramos, se sirve con arroz y ensalada. Con papas a la francesa ó plátanos fritos tiene un costo extra de 35 pesos. El precio es de 145 pesos sin el costo extra.""", "menu.mp3")
    if tipo == 3:
        crearAudio("""
                   El menú en la sección de Camarones es: Platillo 1: Camarones a la diabla. Descripción: camarones en salsa de chile de arbol, guajillo, fritos en mantequilla. el precio es de 185 pesos.
                    Platillo 2: Camarones empanizados. Descripción camarones fritos con pan molido. el precio es de 175 pesos.""", "menu.mp3")
    

