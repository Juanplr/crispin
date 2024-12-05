import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QPushButton, QLabel, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os

# Clase del hilo para el reconocimiento de voz
class SpeechRecognitionThread(QThread):
    recognized_text = pyqtSignal(str)  # Señal para enviar el texto reconocido a la interfaz gráfica

    def __init__(self):
        super().__init__()
        self.running = True  # Bandera para detener el hilo si es necesario

    def run(self):
        bot = "ultron"

        # Crear un archivo de audio de bienvenida
        self.crearAudio(f'Hola, soy {bot}. Puedes llamarme por mi nombre si necesitas algo, si no sabes qué puedo hacer, solo di comandos.', "mensaje.mp3")

        while self.running:
            phrase = self.fn_speech_recognition()

            if bot in phrase.lower():
                self.crearAudio("¿En qué te puedo ayudar?", 'pregunta.mp3')
                search_query = self.fn_speech_recognition("Diga su solicitud:")

                if "leer el menú" in search_query.lower():
                    self.crearAudio("Claro, te leeré el menú", "pedido.mp3")
                elif "comandos" in search_query.lower():
                    self.crearAudio("Los comandos que puedo ejecutar son leer el menú, pedir un platillo, finalizar orden, leer tu pedido.", "ayuda.mp3")
            else:
                self.recognized_text.emit(phrase)

    def fn_speech_recognition(self, prompt_message="Escuchando..."):
        r = sr.Recognizer()
        r.energy_threshold = 10000
        r.dynamic_energy_threshold = False

        with sr.Microphone() as source:
            print(prompt_message)
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

            try:
                phrase = r.recognize_google(audio, language="es-ES")
                return phrase
            except sr.UnknownValueError:
                return "No entendí lo que dijiste."
            except sr.RequestError as e:
                return f"Error de reconocimiento: {e}"

    def crearAudio(self, cadena, nombre):
        if os.path.exists(nombre):
            os.remove(nombre)
        tts = gTTS(cadena, lang="es")
        tts.save(nombre)
        playsound(nombre)

    def stop(self):
        self.running = False  # Detiene el hilo


# Clase del menú principal
class RestaurantMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Palapa Crispin")
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QPushButton {
                background-color: #FFCC66;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #FFD54F;
            }
        """)

        # Widget principal
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Barra de categorías
        category_bar = QWidget()
        category_layout = QHBoxLayout()
        
        categories = ["Bebidas", "Pescados", "Camarones"]
        self.category_buttons = []
        for category in categories:
            button = QPushButton(category)
            button.setStyleSheet("""
                background-color: #4FC3F7;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 10px;
                margin: 5px;
            """)
            button.clicked.connect(self.on_category_clicked)
            self.category_buttons.append(button)
            category_layout.addWidget(button)
        
        category_bar.setLayout(category_layout)
        main_layout.addWidget(category_bar)

        # Área de productos
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.products_layout = QGridLayout()  # Usamos un QGridLayout para organizar los productos
        scroll_content.setLayout(self.products_layout)
        self.scroll.setWidget(scroll_content)
        main_layout.addWidget(self.scroll)

        # Actualizar con productos iniciales
        self.update_product_cards("Bebidas")

        # Pie de página (logo)
        bottom_bar = QWidget()
        bottom_layout = QHBoxLayout()
        
        logo = QLabel()
        logo.setFixedSize(100, 100)
        
        # Cargar la imagen "Palapa.jpg" y asignarla al QLabel
        pixmap = QPixmap("Palapa.jpg")  # Asegúrate de que la imagen esté en el mismo directorio que tu script
        logo.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))  # Escalar la imagen al tamaño del QLabel
        
        logo.setStyleSheet("background-color: #FFE082; border-radius: 50%;")
        bottom_layout.addWidget(logo)
        
        bottom_layout.addStretch()
        
        # Botón de finalizar orden
        finish_button = QPushButton("Finalizar Orden")
        finish_button.setStyleSheet("""
            background-color: #0288D1;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
        """)
        finish_button.setFixedSize(200, 40)
        bottom_layout.addWidget(finish_button)
        
        bottom_bar.setLayout(bottom_layout)
        main_layout.addWidget(bottom_bar)

        # Configurar el widget principal
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Hilo de reconocimiento de voz
        self.speech_thread = SpeechRecognitionThread()
        self.speech_thread.recognized_text.connect(self.handle_recognized_text)
        self.speech_thread.start()

    def on_category_clicked(self):
        sender = self.sender()
        category = sender.text()
        self.update_product_cards(category)

    def update_product_cards(self, category):
        # Limpiar los productos actuales
        for i in reversed(range(self.products_layout.count())):
            widget = self.products_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Definir productos por categoría
        if category == "Bebidas":
            products = [("Coca Cola", "Refresco sabor cola.", 20, "Coca.jpg"),
                        ("Piña Colada", "Cóctel tropical con piña y vodka.", 50, "Pina.jpg")]
        elif category == "Pescados":
            products = [("Mojarra Frita", "Pescado frito.", 150, "Mojarra.jpg"),
                        ("Filete Empanizado", "Filete empanizado fresco.", 180, "Filete.jpg")]
        elif category == "Camarones":
            products = [("Camarones al Mojo", "Camarones en ajo.", 180, "Camarones.jpg"),
                        ("Camarones Empanizados", "Camarones crujientes empanizados.", 175, "CamaronesE.jpg")]
        else:
            products = []

        # Crear nuevas tarjetas con los productos de la categoría seleccionada
        row = 0
        col = 0
        for name, description, price, image_path in products:
            card = ProductCard(name, description, price, image_path)
            self.products_layout.addWidget(card, row, col)
            col += 1
            if col > 2:  # Ajusta la cantidad de productos por fila
                col = 0
                row += 1

    def handle_recognized_text(self, phrase):
        print(f"Comando recibido: {phrase}")
        if "bebidas" in phrase.lower():
            self.update_product_cards("Bebidas")
        elif "pescados" in phrase.lower():
            self.update_product_cards("Pescados")
        elif "camarones" in phrase.lower():
            self.update_product_cards("Camarones")

    def closeEvent(self, event):
        self.speech_thread.stop()
        self.speech_thread.wait()
        super().closeEvent(event)


class ProductCard(QFrame):
    def __init__(self, name, description, price, image_path):
        super().__init__()
        self.setObjectName("productCard")
        self.setStyleSheet("""
            #productCard {
                background-color: #B3E5FC;
                border-radius: 15px;
                padding: 10px;
                margin: 10px;
            }
            QPushButton {
                background-color: #FFE082;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFD54F;
            }
        """)

        layout = QVBoxLayout()
        
        # Nombre del platillo
        name_label = QLabel(name)
        name_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(name_label)

        # Descripción
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Imagen del platillo
        image_placeholder = QLabel()
        image = QPixmap(image_path)  # Cargar la imagen desde el archivo
        image_placeholder.setPixmap(image.scaled(200, 150, Qt.KeepAspectRatio))  # Escalar la imagen al tamaño deseado
        image_placeholder.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_placeholder)

        # Precio
        price_label = QLabel(f"Precio ${price}")
        price_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(price_label)

        # Botón de pedir
        order_button = QPushButton("Pedir")
        layout.addWidget(order_button)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RestaurantMenu()
    window.resize(1024, 768)
    window.show()
    sys.exit(app.exec_())
