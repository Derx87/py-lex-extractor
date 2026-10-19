import json
import re
from bs4 import BeautifulSoup
import requests
"""Esse script é um extrator inteligente feito em Python
que utiliza técnicas de Web Scraping (raspagem de dados web)
para transformar o texto bruto de uma lei oficial do governo
em uma estrutura de dados limpa e organizada em formato JSON."""

def extrair_lei(url, arquivo_saida="lei_estruturada.json"):
  print(f"Baixando dados de: {url}")

  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PyLexExtractor/1.0"
  }
  response = requests.get(url, headers=headers)

  if response.status_code != 200:
    print(f"Erro ao acessar a página. Código: {response.status_code}")
    return

  # Garante a codificação correta dos caracteres em português
  response.encoding = response.apparent_encoding
  soup = BeautifulSoup(response.text, "html.parser")

  artigos = []
  # Expressão regular para identificar o início de um artigo (ex: "Art. 1º", "Art. 10")
  padrao_artigo = re.compile(r"^Art\.\s*\d+[º°]?", re.IGNORECASE)

  for p in soup.find_all(["p", "span"]):
    texto = p.get_text(strip=True)
    if padrao_artigo.match(texto):
      artigos.append({
          "artigo": texto,
          "incidencia_questoes": 0,  # Preparado para o mapa de calor futuro
      })

  print(f"Sucesso! {len(artigos)} artigos encontrados.")

  # Salva em formato JSON
  with open(arquivo_saida, "w", encoding="utf-8") as f:
    json.dump(artigos, f, ensure_ascii=False, indent=4)

  print(f"Dados salvos com sucesso em '{arquivo_saida}'.")


if __name__ == "__main__":
  # Exemplo: Lei de Acesso à Informação (LAI)
  url_exemplo = (
      "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm"
  )
  extrair_lei(url_exemplo)