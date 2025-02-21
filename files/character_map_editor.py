from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QFileDialog, QMessageBox
)
import json

class CharacterMapEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Tablo başlığı
        table_label = QLabel("Karakter Eşleştirme Tablosu")
        table_label.setObjectName("logLabel")
        layout.addWidget(table_label)
        
        # Tablo
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Değiştirilecek Karakter", "Yeni Karakter"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        # Butonlar
        button_layout = QHBoxLayout()
        
        add_button = QPushButton("Yeni Eşleştirme")
        add_button.clicked.connect(self.add_row)
        add_button.setObjectName("actionButton")
        
        remove_button = QPushButton("Seçiliyi Sil")
        remove_button.clicked.connect(self.remove_selected_row)
        remove_button.setObjectName("actionButton")
        
        save_button = QPushButton("Kaydet")
        save_button.clicked.connect(self.save_mappings)
        save_button.setObjectName("saveButton")
        
        load_button = QPushButton("Yükle")
        load_button.clicked.connect(self.load_mappings)
        load_button.setObjectName("actionButton")
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(load_button)
        
        layout.addLayout(button_layout)
        
    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(""))
        self.table.setItem(row_position, 1, QTableWidgetItem(""))
            
    def remove_selected_row(self):
        selected_rows = set(item.row() for item in self.table.selectedItems())
        for row in sorted(selected_rows, reverse=True):
            self.table.removeRow(row)
            
    def get_mappings(self):
        mappings = {}
        for row in range(self.table.rowCount()):
            source = self.table.item(row, 0)
            target = self.table.item(row, 1)
            if source and target and source.text() and target.text():
                mappings[source.text()] = target.text()
        return mappings
        
    def set_mappings(self, mappings):
        self.table.setRowCount(0)
        for source, target in mappings.items():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(source))
            self.table.setItem(row_position, 1, QTableWidgetItem(target))
            
    def save_mappings(self):
        mappings = self.get_mappings()
        if not mappings:
            QMessageBox.warning(self, "Uyarı", "Kaydedilecek eşleştirme bulunamadı!")
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Eşleştirmeleri Kaydet", "", "JSON files (*.json)"
        )
        
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(mappings, f, ensure_ascii=False, indent=4)
                QMessageBox.information(self, "Başarılı", "Eşleştirmeler kaydedildi!")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Kaydetme hatası: {str(e)}")
            
    def load_mappings(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Eşleştirmeleri Yükle", "", "JSON files (*.json)"
        )
        
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    mappings = json.load(f)
                self.set_mappings(mappings)
                QMessageBox.information(self, "Başarılı", "Eşleştirmeler yüklendi!")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya yükleme hatası: {str(e)}")