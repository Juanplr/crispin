import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QScrollArea, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon


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
        self.name = name
        self.price = float(price)  
        self.add_to_cart_callback = add_to_cart_callback 
        
        self.setFixedWidth(400)
        
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
        order_button.clicked.connect(self.on_order_button_clicked)  # Conectar evento
        layout.addWidget(order_button)

        self.setLayout(layout)

    def on_order_button_clicked(self):
        # Llamar al callback de la ventana principal para agregar el precio al carrito
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

   
        self.cart = []  
        self.total = 0.0  
        
        # Widget principal
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Barra de categorías
        category_bar = QWidget()
        category_bar.setObjectName("categoryBar")
        category_layout = QHBoxLayout()

        categories = [
            ("Bebidas", "Refresco.webp"),
            ("Pescados", "Pescado.webp"),
            ("Camarones", "Camarones.webp")
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

       
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.products_layout = QHBoxLayout()
        self.products_layout.setSpacing(10)

        self.update_product_cards("Bebidas")

        scroll_content.setLayout(self.products_layout)
        self.scroll.setWidget(scroll_content)
        main_layout.addWidget(self.scroll)

        # Barra inferior
        bottom_bar = QWidget()
        bottom_layout = QHBoxLayout()

        logo = QLabel()
        logo.setFixedSize(100, 100)
        pixmap = QPixmap("Palapa.jpg")  # Usar la imagen "Palapa.jpg"
        logo.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        logo.setStyleSheet("background-color: #FFE082; border-radius: 50%;")
        bottom_layout.addWidget(logo)

        bottom_layout.addStretch()

       
        self.total_label = QLabel(f"Total: ${self.total}")
        bottom_layout.addWidget(self.total_label)

        
        finish_button = QPushButton("Finalizar Orden")
        finish_button.setObjectName("finishButton")
        finish_button.setFixedSize(200, 40)
        finish_button.clicked.connect(self.finalize_order) 
        bottom_layout.addWidget(finish_button)

        bottom_bar.setLayout(bottom_layout)
        main_layout.addWidget(bottom_bar)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def on_category_clicked(self):
        sender = self.sender()
        category = sender.text()
        self.update_product_cards(category)

    def update_product_cards(self, category):
        for i in reversed(range(self.products_layout.count())):
            widget = self.products_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

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

        for name, description, price, image_path in products:
            card = ProductCard(name, description, price, image_path, self.add_to_cart)
            self.products_layout.addWidget(card)

    def add_to_cart(self, name, price):
        """Agregar el producto al carrito y actualizar el total"""
        self.cart.append((name, price))
        self.total += price
        self.total_label.setText(f"Total: ${self.total:.2f}") 

    def finalize_order(self):
        """Mostrar el resumen de la compra y el total"""
  
        product_list = "\n".join([f"{name} - ${price}" for name, price in self.cart])
        message = f"Has pedido:\n{product_list}\n\nTotal: ${self.total:.2f}"
        
      
        msg_box = QMessageBox()
        
     
        custom_icon = QIcon("Palapa.jpg")  
        msg_box.setIconPixmap(custom_icon.pixmap(QSize(50, 50))) 

        msg_box.setWindowTitle("Resumen de la Orden")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RestaurantMenu()
    window.resize(1200, 600)
    window.show()
    sys.exit(app.exec_())
