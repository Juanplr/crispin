import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QScrollArea, QGraphicsDropShadowEffect, QMessageBox)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QPixmap, QIcon
import speech_recognition as sr
import index


class SpeechRecognitionThread(QThread):
    recognized_text = pyqtSignal(str)  # Señal para enviar el texto reconocido a la interfaz gráfica

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        bot = "lucas"

        index.crearAudio(f'Hola, soy {bot}. Puedes llamarme por mi nombre si necesitas algo, si no sabes qué puedo hacer, solo di comandos.', "mensaje.mp3")

        while self.running:
            phrase = self.fn_speech_recognition()
            print("Escuche: " + phrase)
            if bot in phrase.lower():
                index.crearAudio("¿En qué te puedo ayudar?", 'pregunta.mp3')
                search_query = self.fn_speech_recognition("Diga su solicitud:")
                print(search_query)
                if "leer el menú" in search_query.lower():
                    index.crearAudio("Claro, te leeré el menú, permite un minuto", "pedido.mp3")
                    menu_categoria = self.get_current_category() 
                    print(menu_categoria)
                    index.leerMenu(menu_categoria)
                elif "leer categorías" in search_query.lower():
                    index.crearAudio("Claro las categorias del menu son: Bebidas, Pescados y Camarones", "categorias.mp3")
                elif "ir a bebidas" in search_query.lower():
                    index.crearAudio("Muy Bien moviendome a la categoria de bebidas", "moviendo.mp3")
                    self.recognized_text.emit("bebidas")
                    index.crearAudio("Estas en la categoria de bebidas", "moviendo.mp3")
                elif "ir a pescados" in search_query.lower():
                    index.crearAudio("Muy Bien moviendome a la categoria de Pescados", "moviendo.mp3")
                    self.recognized_text.emit("pescados")
                    index.crearAudio("Estas en la categoria de Pescados", "moviendo.mp3")
                elif "ir a camarones" in search_query.lower():
                    index.crearAudio("Muy Bien moviendome a la categoria de Camarones", "moviendo.mp3")
                    self.recognized_text.emit("camarones")
                    index.crearAudio("Estas en la categoria de Camarones", "moviendo.mp3")
                elif "agrega una coca-cola" in search_query.lower():
                    index.crearAudio("Claro agregare una cocacola a la orden", "agregar.mp3")
                    self.recognized_text.emit("agegar c")
                    index.crearAudio("Cocacola Agregada", "agregar.mp3")
                elif "agrega una piña colada" in search_query.lower():
                    index.crearAudio("Claro agregare una piña colada a la orden", "agregar.mp3")
                    self.recognized_text.emit("agegar pc")
                    index.crearAudio("Piña colada Agregada", "agregar.mp3")
                elif "agrega una mojarra frita" in search_query.lower():
                    index.crearAudio("Claro agregare una mojarra frita a la orden", "agregar.mp3")
                    self.recognized_text.emit("agegar mf")
                    index.crearAudio("mojarra frita Agregada", "agregar.mp3")
                elif "agrega un filete empanizado" in search_query.lower():
                    index.crearAudio("Claro agregare un filete empanizado a la orden", "agregar.mp3")
                    self.recognized_text.emit("agegar fe")
                    index.crearAudio("Filete empanizado Agregado", "agregar.mp3")
                elif "agrega unos camarones a la diabla" in search_query.lower():
                    index.crearAudio("Claro agregare unos camarones a la diabla a la orden", "agregar.mp3")
                    self.recognized_text.emit("agegar diabla")
                    index.crearAudio("camarones a la diabla Agregados", "agregar.mp3")
                elif "agrega unos camarones empanizados" in search_query.lower():
                    index.crearAudio("Claro agregare unos camarones empanizados a la orden", "agregar.mp3")
                    self.recognized_text.emit("agegar emp")
                    index.crearAudio("camarones empanizados Agregados", "agregar.mp3")
                elif "finalizar orden" in search_query.lower():
                    index.crearAudio("¿Estas seguro de finalizar tu orden?", "confirmacion.mp3")
                    confimacion = self.fn_speech_recognition("confirme:")
                    print(confimacion)
                    if "sí" in confimacion.lower():
                        index.crearAudio("Finalizando Orden", "confirmacion.mp3")
                        self.recognized_text.emit("finalizar")
                        index.crearAudio("Orden finalizada espere su comida", "confirmacion.mp3")
                    else:
                        index.crearAudio("Orden no finalizada", "confirmacion.mp3")
                elif "leer orden" in search_query.lower():
                    self.recognized_text.emit("leer orden")
                else: 
                    index.crearAudio("Lo siento no entendi la petición", "error.mp3")
            elif "comandos" in phrase.lower():
                index.crearAudio("Los comandos que puedo ejecutar son leer las categorias del menu, leer el menú, agregar un platillo a la orden y finalizar orden.", "ayuda.mp3")
            QThread.msleep(500) 

    def fn_speech_recognition(self, prompt_message="Escuchando..."):
        r = sr.Recognizer()
        r.energy_threshold = 3000  
        r.dynamic_energy_threshold = True


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
        self.running = False


class ProductCard(QFrame):
    def __init__(self, name, description, price, image_path, add_to_cart_callback):
        super().__init__()
        self.setObjectName("productCard")
        
        self.setStyleSheet("""
            #productCard {
                background-color: #B3E5FC;
                border-radius: 15px;
                padding: 10px;
                margin: 10px;
            }
            QLabel {
                color: #000000;
                background-color: rgba(255, 255, 255, 0.0);
                border-radius: 5px;
                padding: 5px;
                font-size: 16px;
            }
            QPushButton {
                background-color: #FFE082;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                color: #000000;
                border: 1px solid #FF9800;
                font-size: 16px;  
            }
            QPushButton:hover {
                background-color: #FFD54F;
            }
        """)

        self.setFixedWidth(400)
        self.name = name
        self.price = float(price)
        self.add_to_cart_callback = add_to_cart_callback
        
        layout = QVBoxLayout()
        
        name_label = QLabel(name)
        name_label.setFont(QFont("Arial", 12, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)

        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)

        image_placeholder = QLabel()
        image = QPixmap(image_path)
        image_placeholder.setPixmap(image.scaled(150, 100, Qt.KeepAspectRatio))
        image_placeholder.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_placeholder)

        price_label = QLabel(f"Precio ${price}")
        price_label.setFont(QFont("Arial", 11, QFont.Bold))
        price_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(price_label)

        order_button = QPushButton("Pedir")
        order_button.clicked.connect(self.on_order_button_clicked)
        layout.addWidget(order_button)

        self.apply_shadow_effect(self)

        self.setLayout(layout)

    def apply_shadow_effect(self, widget):
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setOffset(5, 5)
        shadow_effect.setColor(Qt.black)
        widget.setGraphicsEffect(shadow_effect)

    def on_order_button_clicked(self):
        self.add_to_cart_callback(self.name, self.price)


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
            }
            QPushButton#categoryButton {
                background-color: rgba(255, 224, 128, 1);
                border-radius: 10px;
                padding: 15px;  /* Incrementé el padding */
                font-weight: bold;
                font-size: 16px;  /* Aumenté el tamaño de la fuente */
                margin: 5px;
                color: #000000;  
            }
            QPushButton#categoryButton:hover {
                background-color: #FFD54F;
            }
            #finishButton {
                background-color: #0288D1;
                color: white;  /* Cambié el texto a blanco */
                border-radius: 10px;
                padding: 20px 40px; 
                font-weight: bold; 
                font-size: 22px;  /* Aumenté el tamaño de la fuente */
                margin-left: -20px;
            }
            #finishButton:hover {
                background-color: #0277BD;
            }
            #bottomBar {
                background-color: rgba(246,190,56,0.9);  
                padding: 10px;
                border-radius: 10px;
                margin-top: 10px;
            }
            #scrollArea {
                background-color: #FFFFFF;
                padding: 10px;
                border-radius: 10px;
            }
        """)

        self.cart = []  
        self.total = 0.0  
        self.categoria = 1  # Inicializamos la categoría en "Bebidas" (1)
        self.speech_thread = SpeechRecognitionThread()
        self.speech_thread.recognized_text.connect(self.handle_recognized_text)
        self.speech_thread.get_current_category = self.get_current_category  # Enlazamos la función
        self.speech_thread.start()


        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Barra de categorías
        category_bar = QWidget()
        category_bar.setObjectName("categoryBar")
        category_layout = QHBoxLayout()
        category_layout.setContentsMargins(0, 0, 0, 0)
        category_layout.setSpacing(0)

        categories = [
            ("Bebidas", "image/Refresco.webp"), 
            ("Pescados", "image/Pescado.webp"), 
            ("Camarones", "image/Camarones.webp")
        ]
        
        self.category_buttons = []
        for category, image_path in categories:
            button = QPushButton(category)
            button.setObjectName("categoryButton")
            button.clicked.connect(self.on_category_clicked)

            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                print(f"Error al cargar la imagen: {image_path}")
            else:
                icon = QIcon(pixmap)
                button.setIcon(icon)
                button.setIconSize(QSize(30, 30))

            category_layout.addWidget(button)
            self.category_buttons.append(button)

        category_bar.setLayout(category_layout)
        main_layout.addWidget(category_bar)

        # Área de productos
        scroll = QScrollArea()
        scroll.setObjectName("scrollArea")
        scroll.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: #FFFFFF;") 
        self.products_layout = QHBoxLayout()

        self.products_layout.setSpacing(10)

        self.update_product_cards("Bebidas")

        scroll_content.setLayout(self.products_layout)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # Barra inferior con total y finalizar orden
        bottom_bar = QWidget()
        bottom_bar.setObjectName("bottomBar")
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        logo = QLabel()
        logo.setFixedSize(100, 100)
        pixmap = QPixmap("image/Palapa.jpg")
        logo.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        logo.setStyleSheet("background-color: #FFE082; border-radius: 50%;")
        bottom_layout.addWidget(logo)

        bottom_layout.addStretch()

        self.total_label = QLabel(f"Total: ${self.total:.2f}")
        self.total_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        bottom_layout.addWidget(self.total_label)

        finish_button = QPushButton("Finalizar Orden")
        finish_button.setObjectName("finishButton")
        finish_button.setFixedSize(260, 60)
        finish_button.clicked.connect(self.finalize_order)
        bottom_layout.addWidget(finish_button)

        bottom_bar.setLayout(bottom_layout)
        main_layout.addWidget(bottom_bar)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def update_product_cards(self, category):
        for i in reversed(range(self.products_layout.count())):
            widget = self.products_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        if category == "Bebidas":
            self.categoria = 1  # Cambiamos el número de menú
            products = [
                ("Coca cola", "Refresco de 355 mililitros..", "26", "image/Coca.jpg"),
                ("Piña Colada", "Bebida de 355 mililitros con jugo de piña y crema de coco con alcohol y hielos. .", "125", "image/Piña.jpg")
            ]
        elif category == "Pescados":
            self.categoria = 2  # Cambiamos el número de menú
            products = [
                ("Mojarra Frita", "Aproximadamente un peso de 450 a 500 gramos, se sirve con arroz y ensalada.", "145", "image/Mojarra.jpg"),
                ("Filete empanizado", "Aproximadamente un peso de 450 a 500 gramos, se sirve con arroz y ensalada. Con papas a la francesa ó plátanos fritos tiene un costo extra de 35 pesos. .", "145", "image/Filete.jpg")
            ]
        elif category == "Camarones":
            self.categoria = 3  # Cambiamos el número de menú
            products = [
                ("Camarones a la diablo", "Camarones en salsa de chile de arbol, guajillo, fritos en mantequilla.", "185", "image/Diabla.jpg"),
                ("Camarones empanizados", "Camarones fritos con pan molido.", "175", "image/CamaronesE.jpg")
            ]
        else:
            products = []

        for name, description, price, image_path in products:
            card = ProductCard(name, description, price, image_path, self.add_to_cart)
            self.products_layout.addWidget(card)

    def on_category_clicked(self):
        sender = self.sender()
        category_name = sender.text()
        self.update_product_cards(category_name)
    def add_to_cart(self, name, price):
        self.cart.append((name, price))
        self.total += price
        self.total_label.setText(f"Total: ${self.total:.2f}")

    def finalize_order(self):
        if self.cart:
            """Mostrar el resumen de la compra y el total"""
    
            product_list = "\n".join([f"{name} - ${price}" for name, price in self.cart])
            message = f"Has pedido:\n{product_list}\n\nTotal: ${self.total:.2f}"
            
        
            msg_box = QMessageBox()
            
        
            custom_icon = QIcon("image/Palapa.jpg")  
            msg_box.setIconPixmap(custom_icon.pixmap(QSize(50, 50))) 

            msg_box.setWindowTitle("Resumen de la Orden")
            msg_box.setText(message)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
        else:
            QMessageBox.warning(self, "Carrito vacío", "No has agregado ningún platillo a tu carrito.")
            
    def read_order(self):
        if self.cart:
            # Crear un resumen de la orden
            total_message = f"El total de tu orden es {self.total:.2f} pesos"

            # Leer la orden usando index.crearAudio
            audio_message = f"Tu orden incluye: {', '.join([item[0] for item in self.cart])}. {total_message}."
            index.crearAudio(audio_message, "orden.mp3")
        else:
            index.crearAudio("No has agregado productos al carrito.", "carrito_vacio.mp3")


    def handle_recognized_text(self, text):
        if "bebidas" in text:
            self.update_product_cards("Bebidas")
        elif "pescados" in text:
            self.update_product_cards("Pescados")
        elif "camarones" in text:
            self.update_product_cards("Camarones")
        elif "agegar c" in text:  
            self.add_to_cart("Coca Cola", 26)
        elif "agegar pc" in text: 
            self.add_to_cart("Piña Colada", 125)
        elif "agegar mf" in text:  
            self.add_to_cart("Mojarra Frita", 145)
        elif "agegar fe" in text:  
            self.add_to_cart("Filete Empanizado", 145)
        elif "agegar diabla" in text:  
            self.add_to_cart("Camarones a la Diabla", 185)
        elif "agegar emp" in text:  
            self.add_to_cart("Camarones Empanizados", 175)
        elif "finalizar" in text:
            self.finalize_order()
            self.read_order()
        elif "leer orden" in text:
            self.read_order()
        

    def closeEvent(self, event):
        self.speech_thread.stop()
        self.speech_thread.wait()
        super().closeEvent(event)
        
    def get_current_category(self):
        return self.categoria



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RestaurantMenu()
    window.resize(1200, 600)
    window.show()
    sys.exit(app.exec_())
