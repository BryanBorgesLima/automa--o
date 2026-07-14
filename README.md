# 🛒 Monitor Inteligente de Preços: Amazon Scraper & Alerta

Este é um projeto de automação e inteligência de mercado desenvolvido em Python utilizando o **Selenium**. O script realiza o monitoramento ativo de preços de notebooks diretamente no site da Amazon Brasil, aplica filtros de faixa de preço e envia notificações automáticas por e-mail com os melhores resultados encontrados.

---

## 🎯 Objetivo do Projeto

Eliminar o trabalho manual de pesquisa de preços em e-commerces. A ferramenta entra no site, pesquisa pelo termo desejado, extrai os dados dos produtos mais relevantes, filtra apenas aqueles que estão dentro do orçamento estipulado e gera relatórios automáticos (CSV e e-mail).

---

## 🚀 Funcionalidades

* **Web Scraping Dinâmico:** Navegação automatizada que lida com o carregamento assíncrono (JavaScript) da Amazon usando Selenium.
* **Tratamento de Dados:** Conversão de strings de preços complexas do e-commerce em valores numéricos (`float`) para cálculos e filtros.
* **Filtro Personalizado:** Segmentação inteligente para extrair apenas produtos dentro de uma faixa de preço específica (ex: R$ 1.300 a R$ 6.000).
* **Persistência de Dados (CSV):** Exportação dos resultados em um arquivo `resultados.csv` formatado em `utf-8-sig` (compatibilidade perfeita com Microsoft Excel).
* **Alerta Automatizado por E-mail:** Disparo de um e-mail em formato HTML estilizado contendo a tabela dos produtos selecionados através do protocolo SMTP do Gmail.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Selenium WebDriver** (Interação com o navegador)
* **Webdriver Manager** (Gerenciamento automático do driver do Chrome)
* **SMTPLib / Email Message** (Serviço de envio de e-mails)
* **CSV Lib** (Exportação e manipulação dos dados)

---

## ⚙️ Como Executar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o Python instalado na sua máquina. Em seguida, instale as bibliotecas necessárias:

```bash
pip install selenium webdriver-manager
