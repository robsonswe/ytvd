from PyQt6.QtCore import QObject, pyqtSignal

class DownloadWorker(QObject):
    """Worker para gerenciar o download em uma thread separada."""
    progress = pyqtSignal(int)
    finished = pyqtSignal(str, bool)  # mensagem, é_erro

    def __init__(self, download_manager, youtube_url, format_type, quality):
        super().__init__()
        self.download_manager = download_manager
        self.youtube_url = youtube_url
        self.format_type = format_type
        self.quality = quality

    def run(self):
        """Lida com o processo de download."""
        try:
            response, status_code = self.download_manager.handle_download_request(
                self.youtube_url, self.format_type, self.quality, self.update_progress
            )
            if status_code != 202:
                message = response.get("error", "Falha no download!")
                self.finished.emit(message, True)
            else:
                message = f"Download iniciado: {response['title']}"
                self.finished.emit(message, False)
        except Exception as e:
            self.finished.emit(str(e), True)

    def update_progress(self, percentage):
        """Atualiza o sinal de progresso."""
        self.progress.emit(percentage)