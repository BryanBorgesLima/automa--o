#1.Bibliotecas que usei
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import sys
sys.stdout.reconfigure(encoding="utf-8")
import csv

#Função que configura nosso navegador
def driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    )
    servico = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=servico, options=chrome_options)

#Inicializações basicas que usei:Navegador; Url; Lista de dados
navegador = driver()
url = "https://www.amazon.com.br/s?k=Notebook"
navegador.get(url)
dados = []


#Estrutura de tentativa
try:
    #Raspagem dos produtos da pagina
    produtos = navegador.find_elements(By.XPATH, "//div[@class='sg-col-4-of-4 sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-8 sg-col-4-of-20']")
    print(f"Foi rastreados {len(produtos)} produtos")

    #Raspagem dos nomes através dos produtos
    for produto in produtos:
 
        try:
            preco_int = produto.find_element(By.CLASS_NAME, "a-price-whole").text
            preco_decimal = produto.find_element(By.CLASS_NAME, "a-price-fraction").text

            preco_total = f"R${preco_int},{preco_decimal}"
            preco = float(f"{preco_int.replace('.', '')}.{preco_decimal}")

        except:
            continue

        if 1300 <= preco and preco <= 6000:

            try:
                nome = produto.find_element(By.CSS_SELECTOR, "a h2 span").text
            except:
                nome = "Nome não encontrado"

            dados.append({
                "Nomes": nome,
                "Preços": preco_total
            })


    print(f"{len(dados)} produtos filtrados")

    #Imprimindo a lista de dados no terminal
    for item in dados:
        print(f"Nome:{item['Nomes']}\n")
        print(f"Preco:{item['Preços']}\n")
        print("==" * 40)
                

#Fim do bloco de tentativa      
except Exception as e:
    print(e)

print(dados)
#Bloco de tentativa para criar um arquivo csv
try:
    #Abre/cria um arquivo csv com o nome resultados
    with open('resultados.csv', 'w', encoding="utf-8") as file_results:
        arquivo = csv.DictWriter(
            file_results,
            fieldnames=["Nomes", "Preços"]
        )
    
        arquivo.writeheader()
        arquivo.writerows(dados)
    print("Seu arquivo csv foi criado/escrito com sucesso")
        
except:
    print("Erro em abrir o csv")
    
print("Parabéns, rapagem e arquivo salvo com sucesso")

#Fecha o navegador assim que o codigo todo é executado
navegador.quit()