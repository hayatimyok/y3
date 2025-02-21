from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt
import os

class ModernCharacterConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Karakter Dönüştürücü")
        self.setGeometry(200, 200, 800, 600)
        
        # Merkezi widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Başlık
        title = QLabel("Karakter Dönüştürücü")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: white;
                margin: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Dosya seçme butonu
        self.file_button = QPushButton("Dosya Seç")
        self.file_button.clicked.connect(self.select_file)
        self.file_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        layout.addWidget(self.file_button)
        
        # Karakter tablosu
        self.char_table = QTableWidget()
        self.char_table.setColumnCount(2)
        self.char_table.setHorizontalHeaderLabels(["Orijinal", "Dönüştürülecek"])
        self.char_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.char_table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                color: white;
                border: none;
            }
            QHeaderView::section {
                background-color: #1e1e1e;
                color: white;
                padding: 5px;
                border: 1px solid #3e3e3e;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        layout.addWidget(self.char_table)
        
        # Kontrol butonları
        button_layout = QHBoxLayout()
        
        self.add_row_button = QPushButton("Satır Ekle")
        self.add_row_button.clicked.connect(self.add_row)
        self.add_row_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        
        self.convert_button = QPushButton("Dönüştür")
        self.convert_button.clicked.connect(self.convert_file)
        self.convert_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        
        button_layout.addWidget(self.add_row_button)
        button_layout.addWidget(self.convert_button)
        layout.addLayout(button_layout)
        
        # Varsayılan karakter eşleştirmelerini yükle
        self.load_default_mappings()
        
        # Stil
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: white;
            }
        """)
        
        self.selected_file = None

    def load_default_mappings(self):
        default_mappings = {
            'Ğ': 'ß', 'ş': 'é', 'İ': 'Î',
            'Ş': 'É', 'ğ': 'ê', 'Ç': 'Á',
            'ı': 'ì'
        }
        
        self.char_table.setRowCount(len(default_mappings))
        for i, (orig, conv) in enumerate(default_mappings.items()):
            self.char_table.setItem(i, 0, QTableWidgetItem(orig))
            self.char_table.setItem(i, 1, QTableWidgetItem(conv))

    def add_row(self):
        current_rows = self.char_table.rowCount()
        self.char_table.insertRow(current_rows)

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Dönüştürülecek Dosyayı Seç",
            "",
            "Metin Dosyaları (*.txt);;Tüm Dosyalar (*)"
        )
        
        if file_name:
            self.selected_file = file_name
            self.file_button.setText(f"Seçili Dosya: {os.path.basename(file_name)}")

    def convert_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Hata", "Lütfen bir dosya seçin!")
            return
        
        try:
            # Karakter eşleştirmelerini al
            mappings = {}
            for row in range(self.char_table.rowCount()):
                orig_item = self.char_table.item(row, 0)
                conv_item = self.char_table.item(row, 1)
                
                if orig_item and conv_item and orig_item.text() and conv_item.text():
                    mappings[orig_item.text()] = conv_item.text()
            
            # Dosyayı oku ve dönüştür
            with open(self.selected_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            for orig, conv in mappings.items():
                content = content.replace(orig, conv)
            
            # Yeni dosyayı kaydet
            file_name = os.path.basename(self.selected_file)
            base_name, ext = os.path.splitext(file_name)
            new_file_path = os.path.join(
                os.path.dirname(self.selected_file),
                f"{base_name}_converted{ext}"
            )
            
            with open(new_file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            QMessageBox.information(
                self,
                "Başarılı",
                f"Dosya dönüştürüldü ve kaydedildi:\n{new_file_path}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Hata",
                f"Dosya dönüştürülürken hata oluştu:\n{str(e)}"
            )