from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QSizePolicy, QProgressBar, QComboBox, QWidget
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile
from .constants import CACHE_DIRECTORY

def setup_browser(parent, home_url):
    """Configura e retorna a visualização do navegador."""
    browser_view = QWebEngineView(parent)
    profile = browser_view.page().profile()
    cache_path = CACHE_DIRECTORY

    profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
    profile.setHttpCacheMaximumSize(1024 * 1024 * 100)  # 100 MB cache
    profile.setCachePath(cache_path)

    # Ativa a aceleração de hardware, rolagem suave e outros recursos
    browser_settings = browser_view.settings()
    browser_settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
    browser_settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
    browser_settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
    browser_settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
    browser_settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)

    browser_view.setUrl(QUrl(home_url))
    return browser_view

def create_nav_button(text, icon_name, slot):
    """Método utilitário para criar um botão de navegação."""
    button = QPushButton(text)
    button.setIcon(QIcon.fromTheme(icon_name))
    button.clicked.connect(slot)
    return button

def create_download_button(text, slot):
    """Método utilitário para criar um botão de download."""
    button = QPushButton(text)
    button.setEnabled(False)
    button.clicked.connect(slot)
    return button

def setup_buttons(browser_view, navigate_home, handle_video_download, handle_audio_download):
    """Configura todos os botões da interface."""
    buttons = {}
    
    buttons["back_button"] = create_nav_button(
        "Voltar", "go-previous", browser_view.back)
    buttons["forward_button"] = create_nav_button(
        "Avançar", "go-next", browser_view.forward)
    buttons["refresh_button"] = create_nav_button(
        "Atualizar", "view-refresh", browser_view.reload)
    buttons["home_button"] = create_nav_button(
        "Início", "go-home", navigate_home)

    buttons["download_video_button"] = create_download_button(
        "Baixar Vídeo", handle_video_download)
    buttons["download_audio_button"] = create_download_button(
        "Baixar Áudio", handle_audio_download)

    buttons["quality_combo"] = QComboBox()
    buttons["quality_combo"].addItems(['720p', '1080p', '480p', '360p'])
    
    return buttons

def setup_progress_bar():
    """Configura a barra de progresso do download."""
    progress_bar = QProgressBar()
    progress_bar.setRange(0, 100)
    progress_bar.setTextVisible(True)
    progress_bar.setFormat("Progresso do Download: %p%")
    return progress_bar

def setup_layouts(browser_view, buttons, progress_bar):
    """Configura todos os layouts da interface."""
    main_layout = QVBoxLayout()
    url_layout = QHBoxLayout()
    button_layout = QHBoxLayout()

    url_label = QLabel("URL")
    url_content = QLabel()
    url_content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    url_layout.addWidget(url_label)
    url_layout.addWidget(url_content)

    # Configura layout de botões
    button_layout.addWidget(buttons["back_button"])
    button_layout.addWidget(buttons["forward_button"])
    button_layout.addWidget(buttons["refresh_button"])
    button_layout.addWidget(buttons["home_button"])
    button_layout.addWidget(buttons["download_video_button"])
    button_layout.addWidget(buttons["download_audio_button"])
    button_layout.addWidget(buttons["quality_combo"])

    main_layout.addLayout(url_layout)
    main_layout.addWidget(browser_view)
    main_layout.addLayout(button_layout)
    main_layout.addWidget(progress_bar)

    central_widget = QWidget()
    central_widget.setLayout(main_layout)
    
    return central_widget, url_label, url_content