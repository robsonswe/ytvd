from PyQt6.QtWidgets import QMessageBox
from urllib.parse import urlparse, parse_qs, urlunparse

class DownloadManagerHandler:
    """Manipula solicitações de download e confirmações do usuário."""

    def __init__(self, download_manager, parent):
        self.download_manager = download_manager
        self.parent = parent

    def request_download(self, youtube_url, format_type, quality):
        """Pergunta ao usuário por confirmação antes de iniciar o download."""
        # Tratando o youtube_url para manter apenas o parâmetro 'v'
        youtube_url = self.clean_youtube_url(youtube_url)

        # Cria a mensagem de confirmação
        msg_box = QMessageBox(self.parent)
        msg_box.setWindowTitle(f'Confirmação de Download {format_type.capitalize()}')
        msg_box.setText(f'Você deseja baixar este {format_type}?\n{youtube_url}')
        
        # Define os botões com textos personalizados
        btn_sim = msg_box.addButton('Sim', QMessageBox.ButtonRole.YesRole)
        btn_nao = msg_box.addButton('Não', QMessageBox.ButtonRole.NoRole)
        
        # Exibe a caixa de diálogo
        msg_box.exec()

        # Verifica a resposta do usuário
        if msg_box.clickedButton() == btn_sim:
            self.parent.start_download(youtube_url, format_type, quality)

    def clean_youtube_url(self, url):
        """Extrai apenas o parâmetro 'v' de uma URL do YouTube."""
        # Parseia a URL em seus componentes
        parsed_url = urlparse(url)
        
        # Extrai os parâmetros da query
        query_params = parse_qs(parsed_url.query)
        
        # Verifica se o parâmetro 'v' está presente
        if 'v' in query_params:
            video_id = query_params['v'][0]  # O ID do vídeo
            # Reconstroi a URL com apenas o parâmetro 'v'
            clean_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', f'v={video_id}', ''))
            return clean_url
        else:
            # Se não houver o parâmetro 'v', retorna a URL original
            return url