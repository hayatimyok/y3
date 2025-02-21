from PyQt5.QtCore import QThread, pyqtSignal

class FileLoader(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        
    def run(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                content = []
                file.seek(0, 2)
                file_size = file.tell()
                file.seek(0)
                
                chunk_size = 8192
                bytes_read = 0
                
                while True:
                    data = file.read(chunk_size)
                    if not data:
                        break
                    content.append(data)
                    bytes_read += len(data.encode('utf-8'))
                    progress = int((bytes_read / file_size) * 100)
                    self.progress.emit(progress)
                
                self.finished.emit("".join(content))
        except Exception as e:
            self.finished.emit(f"Hata: {str(e)}")