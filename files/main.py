import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from translation_tool import TranslationTool

def setup_dark_theme(app):
    app.setStyle("Fusion")
    dark_palette = app.palette()
    dark_palette.setColor(dark_palette.Window, QColor(53, 53, 53))
    dark_palette.setColor(dark_palette.WindowText, Qt.white)
    dark_palette.setColor(dark_palette.Base, QColor(15, 15, 15))
    dark_palette.setColor(dark_palette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(dark_palette.ToolTipBase, Qt.white)
    dark_palette.setColor(dark_palette.ToolTipText, Qt.white)
    dark_palette.setColor(dark_palette.Text, Qt.white)
    dark_palette.setColor(dark_palette.Button, QColor(53, 53, 53))
    dark_palette.setColor(dark_palette.ButtonText, Qt.white)
    dark_palette.setColor(dark_palette.BrightText, Qt.red)
    dark_palette.setColor(dark_palette.Link, QColor(42, 130, 218))
    dark_palette.setColor(dark_palette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(dark_palette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)

if __name__ == "__main__":
    app = QApplication([])
    setup_dark_theme(app)
    tool = TranslationTool()
    tool.show()
    app.exec_()