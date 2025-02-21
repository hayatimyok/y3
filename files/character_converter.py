from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QFileDialog, QTableWidget, 
                            QTableWidgetItem, QMessageBox, QHeaderView, QProgressBar)
from PyQt5.QtCore import Qt, QDir
import os

class ModernCharacterConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Harf Dönüştürücü")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("Harf Dönüştürücü")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: white;
                margin: 10px;
            }
        """)
        layout.addWidget(title)

        # Buttons for file/folder selection
        button_layout = QHBoxLayout()
        
        self.file_button = QPushButton("Dosya Seç")
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
        self.file_button.clicked.connect(self.select_file)
        
        self.folder_button = QPushButton("Klasör Seç")
        self.folder_button.setStyleSheet(self.file_button.styleSheet())
        self.folder_button.clicked.connect(self.select_folder)
        
        button_layout.addWidget(self.file_button)
        button_layout.addWidget(self.folder_button)
        layout.addLayout(button_layout)

        # Selected path label
        self.path_label = QLabel("Seçili: ")
        layout.addWidget(self.path_label)

        # Character mapping table
        table_layout = QVBoxLayout()
        headers = ["Orijinal", "Dönüştürülecek"]
        self.char_table = QTableWidget()
        self.char_table.setColumnCount(2)
        self.char_table.setHorizontalHeaderLabels(headers)
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
        table_layout.addWidget(self.char_table)
        layout.addLayout(table_layout)

        # Table control buttons
        control_layout = QHBoxLayout()
        
        self.add_row_button = QPushButton("Satır Ekle")
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
        self.add_row_button.clicked.connect(self.add_row)
        
        self.delete_row_button = QPushButton("Satır Sil")
        self.delete_row_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.delete_row_button.clicked.connect(self.delete_selected_row)
        
        control_layout.addWidget(self.add_row_button)
        control_layout.addWidget(self.delete_row_button)
        layout.addLayout(control_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
            }
        """)
        layout.addWidget(self.progress_bar)

        # Convert button
        self.convert_button = QPushButton("Dönüştür")
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
        self.convert_button.clicked.connect(self.convert)
        layout.addWidget(self.convert_button)

        # Main window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: white;
            }
        """)

        self.selected_path = None
        self.is_folder = False
        self.load_default_mapping()

    def load_default_mapping(self):
        default_mapping = {
            'ß': 'ss', 'é': 'e', 'Î': 'I', 'É': 'E', 'ê': 'e',
            'Á': 'A', 'ì': 'i', 'Ğ': 'G', 'ş': 's', 'İ': 'I',
            'Ş': 'S', 'ğ': 'g', 'Ç': 'C', 'ı': 'i'
        }
        
        self.char_table.setRowCount(len(default_mapping))
        for idx, (orig, conv) in enumerate(default_mapping.items()):
            self.char_table.setItem(idx, 0, QTableWidgetItem(orig))
            self.char_table.setItem(idx, 1, QTableWidgetItem(conv))

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Dönüştürülecek Dosyayı Seç",
            "",
            "Metin Dosyaları (*.txt);;Tüm Dosyalar (*)"
        )
        if file_path:
            self.selected_path = file_path
            self.is_folder = False
            self.path_label.setText(f"Seçili Dosya: {file_path}")

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Dönüştürülecek Klasörü Seç",
            "",
            QFileDialog.ShowDirsOnly
        )
        if folder_path:
            self.selected_path = folder_path
            self.is_folder = True
            self.path_label.setText(f"Seçili Klasör: {folder_path}")

    def add_row(self):
        current_row = self.char_table.rowCount()
        self.char_table.setRowCount(current_row + 1)
        self.char_table.setItem(current_row, 0, QTableWidgetItem(""))
        self.char_table.setItem(current_row, 1, QTableWidgetItem(""))

    def delete_selected_row(self):
        selected_rows = set(item.row() for item in self.char_table.selectedItems())
        if not selected_rows:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek satırı seçin!")
            return
        
        for row in sorted(selected_rows, reverse=True):
            self.char_table.removeRow(row)

    def get_mapping_dict(self):
        mapping = {}
        for row in range(self.char_table.rowCount()):
            orig_item = self.char_table.item(row, 0)
            conv_item = self.char_table.item(row, 1)
            if orig_item and conv_item and orig_item.text() and conv_item.text():
                mapping[orig_item.text()] = conv_item.text()
        return mapping

    def convert_file(self, file_path, mapping):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            for orig, conv in mapping.items():
                content = content.replace(orig, conv)
                
            output_path = os.path.splitext(file_path)[0] + '_converted' + os.path.splitext(file_path)[1]
            
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(content)
                
            return True
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya dönüştürülürken hata oluştu:\n{str(e)}")
            return False

    def convert(self):
        if not self.selected_path:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir dosya veya klasör seçin!")
            return

        mapping = self.get_mapping_dict()
        if not mapping:
            QMessageBox.warning(self, "Uyarı", "Lütfen en az bir karakter eşleştirmesi ekleyin!")
            return

        if self.is_folder:
            txt_files = []
            for root, _, files in os.walk(self.selected_path):
                for file in files:
                    if file.endswith('.txt'):
                        txt_files.append(os.path.join(root, file))
            
            if not txt_files:
                QMessageBox.warning(self, "Uyarı", "Seçili klasörde .txt dosyası bulunamadı!")
                return

            self.progress_bar.setVisible(True)
            self.progress_bar.setMaximum(len(txt_files))
            self.progress_bar.setValue(0)

            success_count = 0
            for idx, file_path in enumerate(txt_files):
                if self.convert_file(file_path, mapping):
                    success_count += 1
                self.progress_bar.setValue(idx + 1)

            self.progress_bar.setVisible(False)
            QMessageBox.information(
                self,
                "Başarılı",
                f"Toplam {len(txt_files)} dosyadan {success_count} tanesi başarıyla dönüştürüldü."
            )
        else:
            if self.convert_file(self.selected_path, mapping):
                QMessageBox.information(
                    self,
                    "Başarılı",
                    f"Dosya dönüştürüldü ve kaydedildi:\n{os.path.splitext(self.selected_path)[0]}_converted{os.path.splitext(self.selected_path)[1]}"
                )