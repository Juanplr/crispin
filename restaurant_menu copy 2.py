import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QScrollArea, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QPixmap, QIcon
import speech_recognition as sr
import index





class SpeechRecognitionThread(QThread):
    recognized_text = pyqtSignal(str)  # Señal para enviar el texto reconocido a la interfaz gráfica

    def __init__(self):
        super().__init__()
        self.running = True  # Bandera para detener el hilo si es necesario

    def run(self):
        bot = "ultron"

        # Crear un archivo de audio de bienvenida
        index.crearAudio(f'Hola, soy {bot}. Puedes llamarme por mi nombre si necesitas algo, si no sabes qué puedo hacer, solo di comandos.', "mensaje.mp3")

        while self.running:
            phrase = self.fn_speech_recognition()
            print("Escuche: " + phrase)
            if bot in phrase.lower():
                index.crearAudio("¿En qué te puedo ayudar?", 'pregunta.mp3')
                search_query = self.fn_speech_recognition("Diga su solicitud:")

                if "leer el menú" in search_query.lower():
                    index.crearAudio("Claro, te leeré el menú", "pedido.mp3")
                    index.leerMenu(1)
            elif "comandos" in phrase.lower():
                index.crearAudio("Los comandos que puedo ejecutar son leer el menú, pedir un platillo, finalizar orden, leer tu pedido.", "ayuda.mp3")
            

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

    def stop(self):
        self.running = False  # Detiene el hilo


class ProductCard(QFrame):
    def __init__(self, name, description, price, image_path):
        super().__init__()
        self.setObjectName("productCard")
        
        # Establecer el estilo básico de la tarjeta sin el borde azul
        self.setStyleSheet("""
            #productCard {
                background-color: #B3E5FC;  /* Fondo azul para las tarjetas */
                border-radius: 15px;
                padding: 10px;
                margin: 10px;
            }
            QLabel {
                color: #000000;  /* Asegurarse de que el texto de las etiquetas sea negro */
                background-color: rgba(255, 255, 255, 0.0);  /* Fondo blanco semi-transparente para mejorar la legibilidad */
                border-radius: 5px;  /* Bordes redondeados en las etiquetas */
                padding: 5px;  /* Relleno alrededor del texto */
            }
            QPushButton {
                background-color: #FFE082;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                color: #000000;  /* Texto negro para los botones */
                border: 1px solid #FF9800;  /* Borde naranjo para los botones */
            }
            QPushButton:hover {
                background-color: #FFD54F;
            }
        """)

        # Establecer el ancho fijo de las tarjetas
        self.setFixedWidth(400)

        layout = QVBoxLayout()
        
        # Nombre del platillo
        name_label = QLabel(name)
        name_label.setFont(QFont("Arial", 12, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)

        # Descripción
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)

        # Imagen del platillo
        image_placeholder = QLabel()
        image = QPixmap(image_path)  # Cargar la imagen desde el archivo
        image_placeholder.setPixmap(image.scaled(150, 100, Qt.KeepAspectRatio))  # Escalar la imagen al tamaño deseado
        image_placeholder.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_placeholder)

        # Precio
        price_label = QLabel(f"Precio ${price}")
        price_label.setFont(QFont("Arial", 11, QFont.Bold))
        price_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(price_label)

        # Botón de pedir
        order_button = QPushButton("Pedir")
        layout.addWidget(order_button)

        # Aplicar sombra a la tarjeta
        self.apply_shadow_effect(self)

        self.setLayout(layout)

    def apply_shadow_effect(self, widget):
        """Aplicar sombra a un widget."""
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)  # Ajustar el radio de difuminado de la sombra
        shadow_effect.setOffset(5, 5)  # Ajustar el desplazamiento de la sombra
        shadow_effect.setColor(Qt.black)  # Establecer el color de la sombra
        widget.setGraphicsEffect(shadow_effect)

class RestaurantMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Palapa Crispin")
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            #categoryBar {
                background-color: rgba(17, 143, 205, 0.7); 
                border-radius: 10px;
                padding: 10px;
                position: fixed;  
                top: 0;  
                left: 0;  
                width: 100%;  
                min-height: 70px;  
                z-index: 1; 
            }
            QPushButton {
                background-color: rgba(255, 224, 128, 1);
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                margin: 0 5px;
                color: #000000;  /* Texto negro para los botones */
            }
            QPushButton:hover {
                background-color: #FFD54F;
            }
            #finishButton {
                background-color: #0288D1;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            #bottomBar {
                background-color: rgba(246,190,56,0.9);  /* Fondo naranja para el pie */
                padding: 10px;
                border-radius: 10px;
                margin-top: 10px;
            }
            #scrollArea {
                background-color: #FFFFFF;  /* Fondo blanco para la zona de productos */
                padding: 10px;
                border-radius: 10px;
            }
        """)

        # Widget principal
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes del layout principal

        # Barra de categorías
        category_bar = QWidget()
        category_bar.setObjectName("categoryBar")
        category_layout = QHBoxLayout()
        category_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes de la barra de categorías
        category_layout.setSpacing(0)  # Eliminar el espacio entre los botones

        # Definir las categorías con las rutas de las imágenes pequeñas
        categories = [
            ("Bebidas", "Refresco.webp"), 
            ("Pescados", "Pescado.webp"), 
            ("Camarones", "Camarones.webp")
        ]
        
        # Crear los botones con las imágenes
        self.category_buttons = []
        for category, image_path in categories:
            button = QPushButton(category)
            button.setObjectName("categoryButton")
            button.clicked.connect(self.on_category_clicked)  # Conectar evento click

            # Cargar y establecer el ícono pequeño
            pixmap = QPixmap(image_path)  # Cargar la imagen desde el archivo
            if pixmap.isNull():
                print(f"Error al cargar la imagen: {image_path}")
            else:
                icon = QIcon(pixmap)  # Convertir a ícono
                button.setIcon(icon)  # Establecer el ícono del botón
                button.setIconSize(QSize(30, 30))  # Ajustar el tamaño del ícono (pequeño)
                
            category_layout.addWidget(button)
            self.category_buttons.append(button)
        
        category_bar.setLayout(category_layout)
        main_layout.addWidget(category_bar)

        # Área de productos (se inicializa con la categoría "Bebidas")
        scroll = QScrollArea()
        scroll.setObjectName("scrollArea")
        scroll.setWidgetResizable(True)

        scroll_content = QWidget()
        self.products_layout = QHBoxLayout()
        
        self.products_layout.setSpacing(10)  # Espacio entre las tarjetas

        # Inicializar con productos de Bebidas
        self.update_product_cards("Bebidas")

        scroll_content.setLayout(self.products_layout)
        scroll_content.setStyleSheet("background-color: #FFFFFF;") 
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # Barra inferior (como antes)
        bottom_bar = QWidget()
        bottom_bar.setObjectName("bottomBar")
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes del layout inferior
        
        # Logo con PixMap
        logo = QLabel()
        logo.setFixedSize(100, 100)  # Tamaño fijo para el logo
        
        # Cargar la imagen "Palapa.jpg" y asignarla al QLabel
        pixmap = QPixmap("Palapa.jpg")  # Asegúrate de que la imagen esté en el mismo directorio que tu script
        logo.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))  # Escalar la imagen al tamaño del QLabel
        
        # Estilo del logo (puedes cambiarlo si lo prefieres)
        logo.setStyleSheet("background-color: #FFE082; border-radius: 50%;")
        bottom_layout.addWidget(logo)
        
        # Espaciador
        bottom_layout.addStretch()
        
        # Botón de finalizar orden
        finish_button = QPushButton("Finalizar Orden")
        finish_button.setObjectName("finishButton")
        finish_button.setFixedSize(200, 40)
        bottom_layout.addWidget(finish_button)
        
        bottom_bar.setLayout(bottom_layout)
        main_layout.addWidget(bottom_bar)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def on_category_clicked(self):
        sender = self.sender()
        category = sender.text()  # Obtener el nombre de la categoría
        self.update_product_cards(category)

    def update_product_cards(self, category):
        # Limpiar los productos actuales
        for i in reversed(range(self.products_layout.count())):
            widget = self.products_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Definir productos por categoría con imágenes
        if category == "Bebidas":
            products = [
                ("Coca cola", "Refresco sabor cola muy refrescante.", "26", "Coca.jpg"),
                ("Piña Colada", "Cóctel tropical con piña y vodka.", "125", "Piña.jpg")
            ]
        elif category == "Pescados":
            products = [
                ("Mojarra", "Pescado de rio.", "145", "Mojarra.jpg"),
                ("Filete empanizado", "Pescado fresco empanizado crujiente.", "145", "Filete.jpg")
            ]
        elif category == "Camarones":
            products = [
                ("Camarones a la diablo", "Camarones frescos picantes con habanero.", "185", "Diabla.jpg"),
                ("Camarones empanizados", "Camarones empanizados crujientes.", "175", "CamaronesE.jpg")
            ]
        else:
            products = []

        # Crear nuevas tarjetas con los productos de la categoría seleccionada
        for name, description, price, image_path in products:
            card = ProductCard(name, description, price, image_path)
            self.products_layout.addWidget(card)
            
        self.speech_thread = SpeechRecognitionThread()
        self.speech_thread.recognized_text.connect(self.handle_recognized_text)
        self.speech_thread.start()
            
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RestaurantMenu()
    window.resize(1200, 600)
    window.show()
    sys.exit(app.exec_())
