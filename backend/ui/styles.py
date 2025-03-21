from PyQt6.QtGui import QFont

def apply_main_styles(window):
    """Aplica estilos gerais para a janela principal."""
    window.setStyleSheet("""
        QMainWindow {
            background-color: #f0f0f0;
        }
        QLabel {
            font-size: 14px;
            color: #333;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            text-align: center;
            font-size: 14px;
            margin: 4px 2px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
        QComboBox {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 5px;
            min-width: 6em;
        }
        QProgressBar {
            border: 2px solid grey;
            border-radius: 5px;
            background-color: #e0e0e0;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #4CAF50;
            width: 20px;
        }
    """)

    font = QFont("Segoe UI", 10)
    window.setFont(font)

def apply_url_label_styles(url_label, url_content):
    """Aplica estilos para os rótulos de URL."""
    for widget in [url_label, url_content]:
        widget.setStyleSheet("""
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 5px;
        """)

def apply_download_button_styles(download_video_button, download_audio_button):
    """Aplica estilos para botões de download."""
    download_video_button.setStyleSheet("""
        QPushButton {
            background-color: #008CBA;
        }
        QPushButton:disabled {
            background-color: #80C5DA;
            color: #CCCCCC;
        }
    """)
    
    download_audio_button.setStyleSheet("""
        QPushButton {
            background-color: #f44336;
        }
        QPushButton:disabled {
            background-color: #F9A19A;
            color: #CCCCCC;
        }
    """)

def apply_nav_button_styles(nav_buttons):
    """Aplica estilos para botões de navegação."""
    nav_button_style = """
        QPushButton {
            background-color: #E0E0E0;
            color: #333333;
            border: 1px solid #CCCCCC;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #D0D0D0;
        }
        QPushButton:pressed {
            background-color: #C0C0C0;
        }
    """
    for button in nav_buttons:
        button.setStyleSheet(nav_button_style)