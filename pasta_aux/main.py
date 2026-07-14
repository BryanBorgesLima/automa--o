from selenium import webdriver as web
import time


navegador = web.Chrome()
navegador.get("https://www.hashtagtreinamentos.com/")
navegador.maximize_window()

botao_verde = navegador.find_element("class name", "botao-verde")                                      


botao_verde.click()

lista_botoes = navegador.find_elements("class name", "header__titulo")


for botoes in lista_botoes:
    if "Assinatura" in botoes.text:
        botoes.click()
        break

abas = navegador.window_handles
navegador.switch_to.window(abas[1])


navegador.get("https://www.hashtagtreinamentos.com/curso-python?tipo=a&src=site&utm_source=site&utm_campaign=programacao&utm_medium=header&utm_content=header-links&conversion=perpetuo-lespy")


nome = navegador.find_element("id", "firstname")
email = navegador.find_element("id", "email")
telefone = navegador.find_element("id", "phone")

nome.send_keys("Bryan Lima")
email.send_keys("bryanlima999@gmail.com")
telefone.send_keys("1199999-9999")

navegador.find_element("class name", "botao-verde").click()

time.sleep(10) 

