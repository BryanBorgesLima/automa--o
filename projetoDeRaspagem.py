# ============================
# Bibliotecas
# ============================
import csv
import sys

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

sys.stdout.reconfigure(encoding="utf-8")


# ============================
# Configuração do navegador
# ============================
def criar_navegador():

    options = Options()

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())

    return webdriver.Chrome(
        service=service,
        options=options
    )


# ============================
# Programa Principal
# ============================
URL = "https://www.amazon.com.br/s?k=Notebook"

dados = []

try:

    navegador = criar_navegador()

    navegador.get(URL)

    # Espera até que os produtos apareçam
    WebDriverWait(navegador, 20).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
        )
    )

    produtos = navegador.find_elements(
        By.CSS_SELECTOR,
        "div[data-component-type='s-search-result']"
    )

    print(f"\nForam encontrados {len(produtos)} produtos.\n")

    for produto in produtos:

        # ---------------- Nome ----------------

        try:
            nome = produto.find_element(
                By.CSS_SELECTOR,
                "h2 span"
            ).text

        except NoSuchElementException:
            nome = "Nome não encontrado"

        # ---------------- Preço ----------------

        try:

            preco_inteiro = produto.find_element(
                By.CLASS_NAME,
                "a-price-whole"
            ).text

            preco_decimal = produto.find_element(
                By.CLASS_NAME,
                "a-price-fraction"
            ).text

            preco_texto = f"R${preco_inteiro},{preco_decimal}"

            # Converte para float
            preco = float(
                f"{preco_inteiro.replace('.', '')}.{preco_decimal}"
            )

        except NoSuchElementException:
            continue

        # ---------------- Filtro ----------------

        if 1300 <= preco <= 6000:

            dados.append({
                "Nome": nome,
                "Preço": preco_texto
            })

   
    print(f"Foram filtrados {len(dados)} produtos.\n")

except TimeoutException:
    print("A página demorou muito para carregar.")

except WebDriverException as erro:
    print(f"Erro do navegador:\n{erro}")

except Exception as erro:
    print(f"Erro inesperado:\n{erro}")

finally:

    if "navegador" in locals():
        navegador.quit()


# ============================
# Mostrar resultados
# ============================
print("\nProdutos encontrados\n")

for i, produto in enumerate(dados, start=1):

    print(f"Produto {i}")
    print(f"Nome : {produto['Nome']}")
    print(f"Preço: {produto['Preço']}")
    print("=" * 70)


# ============================
# Salvar CSV
# ============================
try:

    with open(
        "resultados.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        writer = csv.DictWriter(
            arquivo,
            fieldnames=["Nome", "Preço"]
        )

        writer.writeheader()
        writer.writerows(dados)

    print("\nArquivo CSV salvo com sucesso!")

except PermissionError:
    print("Feche o arquivo resultados.csv e tente novamente.")

except Exception as erro:
    print(f"Erro ao salvar o CSV:\n{erro}")