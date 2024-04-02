import json
import tkinter as tk
from tkinter import simpledialog, filedialog
import os

def multiplicar_objeto_json(objeto_json, quantidade):
    objetos_multiplicados = []
    for i in range(1, quantidade + 1):
        novo_objeto = objeto_json.copy()
        novo_objeto["numeroMatriculaContribuinte"] = f"Teste1.{i}"
        objetos_multiplicados.append(novo_objeto)
    return objetos_multiplicados

def salvar_em_json(lista_objetos, nome_arquivo):
    with open(nome_arquivo, 'w') as f:
        json.dump({"cadastrosContribuintes": lista_objetos}, f, indent=4)

def selecionar_diretorio():
    root = tk.Tk()
    root.withdraw()
    diretorio = filedialog.askdirectory()
    return diretorio

def obter_nome_arquivo(diretorio, nome_arquivo):
    nome_base, extensao = os.path.splitext(nome_arquivo)
    contador = 1
    while os.path.exists(os.path.join(diretorio, f"{nome_base}_{contador}{extensao}")):
        contador += 1
    return f"{nome_base}_{contador}{extensao}"

# Interface gráfica para solicitar a quantidade de objetos e selecionar o diretório de salvamento
root = tk.Tk()
root.withdraw()
quantidade = simpledialog.askinteger("Quantidade de Objetos", "Informe a quantidade de objetos a serem gerados:")
diretorio = selecionar_diretorio()

# Objeto JSON original
objeto_json_original = {
    "dataAtualizacaoCadastral": "2024-01-01",
    "indicativoCadastroAtivo": "S",
    "nomeCompletoContribuinte": "OSVALDO CECILIO",
    "numeroDocumentoContribuinte": "",
    "numeroMatriculaContribuinte": "Teste1.1001",
    "numeroMatriculaContribuinteNovo": "",
    "tipoContribuinte": 1
}

# Multiplicar o objeto JSON
objetos_multiplicados = multiplicar_objeto_json(objeto_json_original, quantidade)

# Nome do arquivo
nome_arquivo = "cadastrosContribuintes.json"
nome_arquivo = obter_nome_arquivo(diretorio, nome_arquivo)
caminho_arquivo = os.path.join(diretorio, nome_arquivo)

# Salvar os objetos gerados em um arquivo JSON
salvar_em_json(objetos_multiplicados, caminho_arquivo)

print(f"{quantidade} objetos gerados e salvos em '{caminho_arquivo}'")
