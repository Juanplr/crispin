import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

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

class RestaurantMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Palapa Crispin")
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            #categoryBar {
                background-color: #4FC3F7;
                padding: 10px;
                border-radius: 10px;
                margin: 10px;
            }
            QPushButton {
                background-color: #FFE082;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                margin: 0 5px;
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
        """)

        # Widget principal
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Barra de categorías
        category_bar = QWidget()
        category_bar.setObjectName("categoryBar")
        category_layout = QHBoxLayout()
        
        # Categorías
        categories = ["Bebidas", "Pescados", "Camarones"]
        self.category_buttons = []
        for category in categories:
            button = QPushButton(category)
            button.setObjectName("categoryButton")
            button.clicked.connect(self.on_category_clicked)  # Conectar el evento de click
            self.category_buttons.append(button)
            category_layout.addWidget(button)
        
        category_bar.setLayout(category_layout)
        main_layout.addWidget(category_bar)

        # Área de productos
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.products_layout = QHBoxLayout()

        # Inicializar con productos de Bebidas
        self.update_product_cards("Bebidas")

        scroll_content.setLayout(self.products_layout)
        self.scroll.setWidget(scroll_content)
        main_layout.addWidget(self.scroll)

        # Barra inferior
        bottom_bar = QWidget()
        bottom_layout = QHBoxLayout()
        
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RestaurantMenu()
    window.resize(1440, 1024)
    window.show()
    sys.exit(app.exec_())
