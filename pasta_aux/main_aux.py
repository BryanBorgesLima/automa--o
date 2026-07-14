# pegar os telefones dos sites
import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# ================= CONFIGURAÇÃO =================
# COLOQUE SUA CHAVE DA OPENAI AQUI
API_KEY = "SUA_CHAVE_API_AQUI" 

# Arquivo de entrada e saída
INPUT_FILE = "sites.txt"
OUTPUT_FILE = "resultado_telefones.csv"

# Modelo da OpenAI (gpt-4o-mini é mais barato e rápido para essa tarefa)
MODELO = "gpt-4o-mini"
# ================================================

# Inicializa o cliente OpenAI
client = OpenAI(api_key=API_KEY)

def limpar_html(html_content):
    """
    Usa BeautifulSoup para remover scripts, estilos e tags desnecessárias,
    retornando apenas o texto visível para economizar tokens.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    if len(soup.text) > 2000:
    # Remove tags que não contêm texto visível ou útil para contato
        for element in soup(["script", "style", "meta", "noscript", "header", "svg", "path"]):
            element.extract()
    return soup

def extrair_telefone_com_ia(texto_site, url):
    """
    Envia o texto do site para a OpenAI identificar o telefone.
    """
    prompt_sistema = (
        "Você é um assistente especialista em extração de dados. "
        "Sua tarefa é encontrar o número de telefone principal de contato comercial no código HTML fornecido de um site. "
        "Se houver vários, prefira celulares (WhatsApp) ou fixos locais. Pesquise dentro dos links (parâmetros href das tags a do html se existe um numero de telefone também, ele pode estar em um parâmetro no link chamado phone= ou algo parecido)"
        "Retorne APENAS o número formatado. Se não encontrar, retorne 'Não encontrado'."
    )

    prompt_usuario = f"URL do site: {url}\n\nConteúdo do site:\n{texto_site}\n\nExtraia o telefone:"

    try:
        response = client.chat.completions.create(
            model=MODELO,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            # temperature=0  # Temperatura 0 para ser o mais preciso possível
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro na IA: {e}"

def processar_sites():
    # Verifica se o arquivo de entrada existe
    if not os.path.exists(INPUT_FILE):
        print(f"Erro: Arquivo '{INPUT_FILE}' não encontrado.")
        return

    # Lê os sites
    with open(INPUT_FILE, 'r', encoding='utf-8') as file:
        sites = [line.strip() for line in file.readlines() if line.strip()]

    print(f"Iniciando extração de {len(sites)} sites...")
    
    # Prepara o arquivo de saída (escreve o cabeçalho)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file_out:
        file_out.write("URL;Telefone Extraido\n")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for site in sites:
        # Garante que tem http/https
        url_alvo = site if site.startswith('http') else f'https://{site}'
        
        print(f"Processando: {url_alvo}...", end="\r")

        try:
            # 1. Baixar o site
            response = requests.get(url_alvo, headers=headers, timeout=15)
            response.raise_for_status()

            # 2. Limpar o HTML
            texto_limpo = limpar_html(response.content)

            # 3. Usar IA para extrair
            telefone = extrair_telefone_com_ia(texto_limpo, url_alvo)

            print(f"[OK] {url_alvo} -> {telefone}")

            # Salvar no arquivo
            with open(OUTPUT_FILE, 'a', encoding='utf-8') as file_out:
                file_out.write(f"{url_alvo};{telefone}\n")

        except requests.exceptions.RequestException as e:
            print(f"[ERRO DE CONEXÃO] {url_alvo}: {e}")
            with open(OUTPUT_FILE, 'a', encoding='utf-8') as file_out:
                file_out.write(f"{url_alvo};Erro de acesso ao site\n")
        
        except Exception as e:
            print(f"[ERRO GERAL] {url_alvo}: {e}")
            with open(OUTPUT_FILE, 'a', encoding='utf-8') as file_out:
                file_out.write(f"{url_alvo};Erro desconhecido\n")

if __name__ == "__main__":
    processar_sites()