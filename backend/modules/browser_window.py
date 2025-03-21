import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt6.QtCore import QUrl, QTimer, pyqtSlot, QThread
from PyQt6.QtWebEngineWidgets import QWebEngineView

from .download_manager import DownloadManager
from .download_worker import DownloadWorker
from .download_manager_handler import DownloadManagerHandler
from .ui_setup import (
    setup_browser, setup_buttons, setup_progress_bar, setup_layouts
)
from .styles import (
    apply_main_styles, apply_url_label_styles, 
    apply_download_button_styles, apply_nav_button_styles
)

class BrowserWindow(QMainWindow):
    """Janela Principal do Navegador com recursos de download de vídeos do YouTube."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube")
        self.download_manager = DownloadManager()
        self.download_handler = DownloadManagerHandler(
            self.download_manager, self)
        self.download_thread = None
        self.download_worker = None

        self.home_url = "https://www.youtube.com"
        self.init_ui()
        self.init_timer()
        self.apply_styles()
        self.showMaximized()

    def init_ui(self):
        """Inicializa o layout e os widgets da interface do usuário."""
        # Inicializa o navegador
        self.browser_view = setup_browser(self, self.home_url)
        
        # Configura os botões
        self.buttons = setup_buttons(
            self.browser_view, 
            self.navigate_home,
            self.handle_video_download_click,
            self.handle_audio_download_click
        )
        
        # Extrai as referências para fácil acesso
        self.back_button = self.buttons["back_button"]
        self.forward_button = self.buttons["forward_button"]
        self.refresh_button = self.buttons["refresh_button"]
        self.home_button = self.buttons["home_button"]
        self.download_video_button = self.buttons["download_video_button"]
        self.download_audio_button = self.buttons["download_audio_button"]
        self.quality_combo = self.buttons["quality_combo"]
        
        # Configura a barra de progresso
        self.progress_bar = setup_progress_bar()
        
        # Configura layouts
        central_widget, self.url_label, self.url_content = setup_layouts(
            self.browser_view, self.buttons, self.progress_bar
        )
        self.setCentralWidget(central_widget)

    def init_timer(self):
        """Inicializa o timer de verificação da URL."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_url_periodically)
        self.timer.start(2000)

    def check_url_periodically(self):
        """Verifica a URL atual e atualiza os estados dos botões de download."""
        current_url = self.browser_view.url().toString()
        self.update_url_label(current_url)

        is_youtube_url = current_url.startswith(
            "https://www.youtube.com/watch?v=") or current_url.startswith("https://youtu.be/")
        self.enable_download_buttons(is_youtube_url)
        if not is_youtube_url:
            self.setWindowTitle("YouTube")

    def update_url_label(self, url):
        """Atualiza o rótulo de exibição da URL."""
        self.url_content.setText(url)

    def enable_download_buttons(self, enable):
        """Habilita ou desabilita os botões de download."""
        self.download_video_button.setEnabled(enable)
        self.download_audio_button.setEnabled(enable)

    def start_download(self, youtube_url, format_type, quality):
        """Inicia o download em uma thread separada."""
        if self.download_thread:
            self.terminate_download_thread()

        self.download_thread = QThread()
        self.download_worker = DownloadWorker(
            self.download_manager, youtube_url, format_type, quality)
        self.download_worker.moveToThread(self.download_thread)

        self.download_thread.started.connect(self.download_worker.run)
        self.download_worker.finished.connect(self.on_download_finished)
        self.download_worker.progress.connect(self.update_progress)

        self.download_thread.start()

    def terminate_download_thread(self):
        """Termina a thread de download se estiver em execução."""
        if self.download_thread:
            self.download_thread.quit()
            self.download_thread.wait()

    def on_download_finished(self, message, is_error):
        """Lida com a conclusão do download."""
        self.terminate_download_thread()
        self.download_worker = None
        self.show_download_status(message, is_error)

    def show_download_status(self, message, is_error=False):
        """Exibe uma mensagem de status para o download."""
        if is_error:
            QMessageBox.critical(self, "Erro no Download", message)
        else:
            QMessageBox.information(self, "Download Iniciado", message)

    def closeEvent(self, event):
        """Lida com a limpeza quando a janela é fechada."""
        self.terminate_download_thread()
        event.accept()

    @pyqtSlot()
    def handle_video_download_click(self):
        """Handle the click event for downloading videos."""
        current_url = self.browser_view.url().toString()
        quality = self.quality_combo.currentText().replace(
            'p', '')  # Remove 'p' to get numeric value
        self.download_handler.request_download(current_url, "video", quality)

    @pyqtSlot()
    def handle_audio_download_click(self):
        """Handle the click event for downloading audio."""
        current_url = self.browser_view.url().toString()
        self.download_handler.request_download(current_url, "audio", "best")

    @pyqtSlot(int)
    def update_progress(self, percentage):
        """Update the progress bar with the current download percentage."""
        self.progress_bar.setValue(percentage)

    @pyqtSlot()
    def navigate_home(self):
        """Navigate back to the home URL."""
        self.browser_view.setUrl(QUrl(self.home_url))

    def apply_styles(self):
        """Apply custom styles to the application."""
        # Aplica estilos gerais
        apply_main_styles(self)
        
        # Aplica estilos para labels de URL
        apply_url_label_styles(self.url_label, self.url_content)
        
        # Aplica estilos para botões de download
        apply_download_button_styles(self.download_video_button, self.download_audio_button)
        
        # Aplica estilos para botões de navegação
        apply_nav_button_styles([
            self.back_button, self.forward_button, 
            self.refresh_button, self.home_button
        ])

    def focusInEvent(self, event):
        """Repaint browser view on focus in."""
        self.browser_view.setVisible(False)
        self.browser_view.setVisible(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        """Hide browser view on focus out."""
        self.browser_view.setVisible(False)
        super().focusOutEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec())