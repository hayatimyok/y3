from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSplitter, QPlainTextEdit, QListWidget, QPushButton,
    QProgressBar, QStatusBar, QMenuBar, QAction, QFontDialog,
    QInputDialog, QMessageBox, QFileDialog, QTabWidget, QDialog,
    QApplication
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QTextCursor
import os
import webbrowser
import pyperclip
from deep_translator import GoogleTranslator
from file_loader import FileLoader
from syntax_highlighter import SyntaxHighlighter
from character_converter import ModernCharacterConverter

class TranslationTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.folder_path = None
        self.current_file_path = None
        self.file_loader = None
        self.last_search = ""
        self.translator = GoogleTranslator(source='auto', target='tr')
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Çeviri Aracı")
        self.setGeometry(100, 100, 1200, 800)
        
        # Merkezi widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Menü bar
        self.create_menu_bar()
        
        # Header
        self.header = QLabel("Çeviri Aracı")
        self.header.setFixedHeight(30)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("""
            QLabel {
                font-size: 14px;
                padding: 5px;
                color: white;
                background-color: #2c3e50;
                border-radius: 5px;
                margin: 2px;
            }
        """)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        self.progress_bar.hide()
        
        # Splitter
        self.splitter = QSplitter(Qt.Horizontal)
        
        # Dosya listesi
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget {
                background-color: #2e2e2e;
                color: white;
                font-size: 14px;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #3498db;
            }
        """)
        self.file_list.itemClicked.connect(self.load_selected_file)
        
        # Text Edit
        self.text_edit = QPlainTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: white;
                font-size: 14px;
                font-family: Consolas;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        
        # Syntax Highlighter
        self.highlighter = SyntaxHighlighter(self.text_edit.document())
        
        # Splitter'a widget'ları ekle
        self.splitter.addWidget(self.file_list)
        self.splitter.addWidget(self.text_edit)
        self.splitter.setSizes([200, 800])
        
        # Kontrol Butonları
        self.controls_layout = QHBoxLayout()
        
        button_style = """
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:disabled {
                background-color: #7f8c8d;
            }
        """
        
        self.load_folder_button = QPushButton("📁 Klasör Yükle")
        self.load_file_button = QPushButton("📄 Dosya Yükle")
        self.save_button = QPushButton("💾 Kaydet")
        self.translate_button = QPushButton("🌐 Çevir")
        self.find_button = QPushButton("🔍 Bul")
        self.char_converter_button = QPushButton("🔠 Harf Dönüştürücü")
        
        buttons = [
            self.load_folder_button, self.load_file_button,
            self.save_button, self.translate_button,
            self.find_button, self.char_converter_button
        ]
        
        for button in buttons:
            button.setStyleSheet(button_style)
            self.controls_layout.addWidget(button)
        
        self.save_button.setEnabled(False)
        self.translate_button.setEnabled(False)
        self.find_button.setEnabled(False)
        
        # Ana layout'a eklemeler
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.progress_bar)
        self.main_layout.addWidget(self.splitter)
        self.main_layout.addLayout(self.controls_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Bağlantılar
        self.load_folder_button.clicked.connect(self.load_folder)
        self.load_file_button.clicked.connect(self.load_file)
        self.save_button.clicked.connect(self.save_file)
        self.translate_button.clicked.connect(self.translate_selection)
        self.find_button.clicked.connect(self.find_text)
        self.char_converter_button.clicked.connect(self.open_char_converter)

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # Dosya menüsü
        file_menu = menubar.addMenu('Dosya')
        
        new_file = QAction('Yeni', self)
        new_file.setShortcut('Ctrl+N')
        new_file.triggered.connect(self.new_file)
        
        open_file = QAction('Aç', self)
        open_file.setShortcut('Ctrl+O')
        open_file.triggered.connect(self.load_file)
        
        save_file = QAction('Kaydet', self)
        save_file.setShortcut('Ctrl+S')
        save_file.triggered.connect(self.save_file)
        
        file_menu.addAction(new_file)
        file_menu.addAction(open_file)
        file_menu.addAction(save_file)
        
        # Düzen menüsü
        edit_menu = menubar.addMenu('Düzen')
        
        change_font = QAction('Yazı Tipi...', self)
        change_font.triggered.connect(self.change_font)
        
        edit_menu.addAction(change_font)
        
        # Görünüm menüsü
        view_menu = menubar.addMenu('Görünüm')
        
        toggle_wrap = QAction('Sözcük Kaydırma', self)
        toggle_wrap.setCheckable(True)
        toggle_wrap.triggered.connect(self.toggle_word_wrap)
        
        view_menu.addAction(toggle_wrap)

    def save_file(self):
        if not self.current_file_path:
            self.current_file_path, _ = QFileDialog.getSaveFileName(
                self, 'Dosyayı Kaydet', '', 
                'Metin Dosyası (*.txt);;Tüm Dosyalar (*)'
            )
        
        if self.current_file_path:
            try:
                with open(self.current_file_path, "w", encoding="utf-8") as file:
                    content = self.text_edit.toPlainText()
                    file.write(content)
                self.status_bar.showMessage('Dosya kaydedildi')
                QMessageBox.information(self, "Başarılı", "Değişiklikler kaydedildi.")
            except Exception as e:
                self.status_bar.showMessage('Dosya kaydedilemedi')
                QMessageBox.critical(
                    self, "Hata",
                    f"Dosya kaydedilirken hata oluştu: {str(e)}"
                )

    def translate_selection(self):
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()
        
        if selected_text:
            try:
                self.status_bar.showMessage('Çeviri yapılıyor...')
                QApplication.processEvents()
                
                translated_text = self.translator.translate(selected_text)
                self.show_translation_dialog(selected_text, translated_text)
                
                self.status_bar.showMessage('Çeviri tamamlandı')
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Çeviri sırasında hata: {str(e)}")
        else:
            QMessageBox.warning(self, "Hata", "Çevrilecek metin seçilmedi.")

    def show_translation_dialog(self, original_text, translated_text):
        dialog = QDialog(self)
        dialog.setWindowTitle("Çeviri Sonucu")
        dialog.setMinimumWidth(500)
        layout = QVBoxLayout()

        # Orijinal metin
        original_label = QLabel("Orijinal Metin:")
        original_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        layout.addWidget(original_label)
        
        original_text_edit = QPlainTextEdit()
        original_text_edit.setPlainText(original_text)
        original_text_edit.setReadOnly(False)
        original_text_edit.setMaximumHeight(100)
        layout.addWidget(original_text_edit)

        # Çeviri
        translated_label = QLabel("Çeviri:")
        translated_label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        layout.addWidget(translated_label)
        
        translated_text_edit = QPlainTextEdit()
        translated_text_edit.setPlainText(translated_text)
        translated_text_edit.setReadOnly(True)
        translated_text_edit.setMaximumHeight(100)
        layout.addWidget(translated_text_edit)

        # Butonlar
        button_layout = QHBoxLayout()
        
        # Kopyala butonu
        copy_button = QPushButton("Çeviriyi Kopyala")
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(translated_text))
        copy_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        # Metne ekle butonu
        insert_button = QPushButton("Metne Ekle")
        insert_button.clicked.connect(lambda: self.insert_translation(translated_text))
        insert_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        
        # Değiştir butonu
        replace_button = QPushButton("Seçili Metni Değiştir")
        replace_button.clicked.connect(lambda: self.replace_selected_text(translated_text))
        replace_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        
        # Kapat butonu
        close_button = QPushButton("Kapat")
        close_button.clicked.connect(dialog.close)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #9E9E9E;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #757575;
            }
        """)
        
        button_layout.addWidget(copy_button)
        button_layout.addWidget(insert_button)
        button_layout.addWidget(replace_button)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QLabel {
                color: white;
                margin-top: 10px;
            }
            QPlainTextEdit {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #333333;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        
        dialog.exec_()

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        self.status_bar.showMessage('Çeviri panoya kopyalandı')

    def insert_translation(self, text):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText('\n' + text)
        self.status_bar.showMessage('Çeviri metne eklendi')

    def replace_selected_text(self, text):
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            cursor.insertText(text)
            self.status_bar.showMessage('Seçili metin çeviri ile değiştirildi')
        else:
            self.status_bar.showMessage('Değiştirilecek metin seçilmedi')

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.status_bar.showMessage(f'Dosya yükleniyor... %{value}')

    def file_loading_finished(self, content):
        self.text_edit.setPlainText(content)
        self.text_edit.setReadOnly(False)
        self.save_button.setEnabled(True)
        self.translate_button.setEnabled(True)
        self.find_button.setEnabled(True)
        self.progress_bar.hide()
        
        if self.current_file_path:
            file_size = os.path.getsize(self.current_file_path) / 1024  # KB
            line_count = len(content.splitlines())
            self.status_bar.showMessage(
                f'Dosya: {os.path.basename(self.current_file_path)} | '
                f'Boyut: {file_size:.1f} KB | '
                f'Satır: {line_count}'
            )

    def load_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Klasör Seç")
        if folder_path:
            self.folder_path = folder_path
            self.file_list.clear()
            
            for file_name in os.listdir(folder_path):
                if file_name.endswith((".txt", ".csv", ".json")):
                    self.file_list.addItem(file_name)
            
            self.status_bar.showMessage(f'{len(os.listdir(folder_path))} dosya bulundu')

    def load_file(self, file_path=None):
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Dosya Seç", "", 
                "Desteklenen Dosyalar (*.txt *.csv *.json);;Tüm Dosyalar (*)"
            )
        
        if file_path:
            self.current_file_path = file_path
            self.text_edit.clear()
            self.progress_bar.show()
            self.progress_bar.setValue(0)
            
            self.file_loader = FileLoader(file_path)
            self.file_loader.progress.connect(self.update_progress)
            self.file_loader.finished.connect(self.file_loading_finished)
            self.file_loader.start()

    def load_selected_file(self, item):
        if not self.folder_path:
            return
        
        file_path = os.path.join(self.folder_path, item.text())
        if os.path.exists(file_path):
            self.load_file(file_path)

    def new_file(self):
        self.text_edit.clear()
        self.text_edit.setReadOnly(False)
        self.current_file_path = None
        self.save_button.setEnabled(True)
        self.translate_button.setEnabled(True)
        self.find_button.setEnabled(True)
        self.status_bar.showMessage('Yeni dosya oluşturuldu')

    def change_font(self):
        font, ok = QFontDialog.getFont(self.text_edit.font(), self)
        if ok:
            self.text_edit.setFont(font)

    def toggle_word_wrap(self, checked):
        self.text_edit.setLineWrapMode(
            QPlainTextEdit.WidgetWidth if checked else QPlainTextEdit.NoWrap
        )

    def find_text(self):
        text, ok = QInputDialog.getText(
            self, 'Metin Bul',
            'Aranacak metin:',
            text=self.last_search
        )
        
        if ok and text:
            self.last_search = text
            cursor = self.text_edit.document().find(text)
            if not cursor.isNull():
                self.text_edit.setTextCursor(cursor)
            else:
                QMessageBox.information(
                    self, "Sonuç",
                    f"'{text}' metni bulunamadı."
                )

    def open_char_converter(self):
        self.char_converter = ModernCharacterConverter()
        self.char_converter.show()

    def closeEvent(self, event):
        if self.text_edit.document().isModified():
            reply = QMessageBox.question(
                self, 'Çıkış',
                'Kaydedilmemiş değişiklikler var. Kaydetmek ister misiniz?',
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )

            if reply == QMessageBox.Save:
                self.save_file()
                event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

if __name__ == '__main__':
    app = QApplication([])
    tool = TranslationTool()
    tool.show()
    app.exec_()