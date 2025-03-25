import os
import sys
import requests
import zipfile
import argparse
from tqdm import tqdm

def parse_args():
    """Parse command-line arguments with help messages."""
    parser = argparse.ArgumentParser(description="Update the YTVD application by downloading and extracting the latest version.")
    parser.add_argument(
        "--ytvd-folder",
        required=True,
        help="Directory where the YTVD application is installed (e.g., YTVD2)."
    )
    parser.add_argument(
        "--version-file",
        required=True,
        help="File to store the current version number (e.g., version.txt)."
    )
    parser.add_argument(
        "--zip-url",
        required=True,
        help="URL to download the latest YTVD ZIP file (e.g., https://github.com/robsonswe/ytvd/releases/latest/download/YTVD2.zip)."
    )
    parser.add_argument(
        "--github-api-url",
        required=True,
        help="GitHub API URL to fetch the latest release information (e.g., https://api.github.com/repos/robsonswe/ytvd/releases/latest)."
    )
    parser.add_argument(
        "--download-zip",
        default="YouTubeDownloader.zip",
        help="Temporary file name for the downloaded ZIP (default: YouTubeDownloader.zip)."
    )
    return parser.parse_args()

def get_remote_version(github_api_url):
    """Fetch the latest version number from the GitHub API."""
    print("Obtendo versao remota...")
    try:
        response = requests.get(github_api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        remote_version = data.get("tag_name")
        if not remote_version:
            print("Erro: 'tag_name' nao encontrado na resposta da API.")
            sys.exit(1)
        return remote_version
    except requests.RequestException as e:
        print(f"Erro ao acessar a API do GitHub: {e}")
        sys.exit(1)

def get_local_version(version_file):
    """Read the local version number from the version file."""
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            return f.read().strip()
    return "0.0.0"  # Default for first run or missing file

def download_and_extract_zip(zip_url, download_zip):
    """Download the ZIP file with a progress bar and extract it."""
    try:
        response = requests.get(zip_url, stream=True, timeout=10)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        block_size = 8192  # 8 KB chunks
        with open(download_zip, "wb") as f:
            with tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc="Baixando atualização"
            ) as pbar:
                for data in response.iter_content(block_size):
                    f.write(data)
                    pbar.update(len(data))
    except requests.RequestException as e:
        print(f"Erro ao baixar o arquivo ZIP: {e}")
        sys.exit(1)

    print("Extraindo o arquivo ZIP...")
    try:
        with zipfile.ZipFile(download_zip, "r") as zip_ref:
            zip_ref.extractall(".")  # Extracts to current directory
        os.remove(download_zip)
    except zipfile.BadZipFile as e:
        print(f"Erro: Arquivo ZIP corrompido ou invalido: {e}")
        os.remove(download_zip)
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao extrair o arquivo ZIP: {e}")
        os.remove(download_zip)
        sys.exit(1)

def save_version(version_file, version):
    """Save the version number to the version file."""
    with open(version_file, "w") as f:
        f.write(version)

def main():
    """Main function to check for updates and perform the update if necessary."""
    args = parse_args()
    print("==============================")
    print("Verificando atualizacoes...")
    print("==============================")

    remote_version = get_remote_version(args.github_api_url)
    print(f"Versao remota: {remote_version}")

    if not os.path.exists(args.ytvd_folder):
        print(f"Diretorio {args.ytvd_folder} nao encontrado.")
        download_and_extract_zip(args.zip_url, args.download_zip)
        save_version(args.version_file, remote_version)
        print(f"Versao inicial instalada: {remote_version}")
    else:
        local_version = get_local_version(args.version_file)
        print(f"Versao local: {local_version}")
        if local_version != remote_version:
            print("Atualizacao encontrada!")
            download_and_extract_zip(args.zip_url, args.download_zip)
            save_version(args.version_file, remote_version)
            print("Atualizacao concluida!")
        else:
            print("Nenhuma atualizacao disponivel.")

    sys.exit(0)  # Indicate successful execution

if __name__ == "__main__":
    main()