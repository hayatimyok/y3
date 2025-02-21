from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
import re

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []
        self.setup_rules()
        
    def setup_rules(self):
        tag_format = QTextCharFormat()
        tag_format.setForeground(QColor("red"))
        tag_format.setFontWeight(QFont.Bold)
        
        key_format = QTextCharFormat()
        key_format.setForeground(QColor("#FFD700"))  # Altın sarısı
        
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#98FB98"))  # Açık yeşil
        
        self.rules = [
            (r'\[.*?\]', tag_format),  # Köşeli parantez içindekiler
            (r'".*?"', string_format),  # Tırnak içindeki metinler
            (r'[A-Z][A-Za-z]*:', key_format),  # Büyük harfle başlayan kelimeler
        ]
    
    def highlightBlock(self, text):
        for pattern, format in self.rules:
            for match in re.finditer(pattern, text):
                start = match.start()
                length = match.end() - match.start()
                self.setFormat(start, length, format)