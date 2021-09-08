## Projeto tradução Pathfinder: King Maker  ##
#   Criado por:                              #
#   Luiz Filipe Azeredo (Eskimogamepro)          #
#   Renant Bernabe (Mutar)                   #
#   Criado em 25/08/2020                     #
##############################################
import os
import glob
import json
import shutil
import time
import datetime
import re
from pprint import pprint
from googletrans import Translator

# Variaveis de configuração
cwd = os.getcwd() 
versaoAtual = '2-1-4' # Defina a nova versão para ser traduzida
versaoAnterior = 'old' # Defina a ultima versão traduzida
arquivoTraducao = 'enG*'

# Inicia a lib de tradução
translator = Translator()

# Traduz o texto
def traduzir(texto):
    try:
        print("traduzindo texto...")
        texto = reduzCaracter(texto)
        texto = translator.translate(texto, dest='pt').text
        time.sleep(0.3)

        return texto
    except:
        print('Erro: Mude seu IP - ' + str(datetime.datetime.now()))
        time.sleep(5)
        return traduzir(texto)
    

# Reduzir caracteres
def reduzCaracter(texto):
    texto = texto.lower()
    return texto
  
# Remove TAG HTML
def removeTagHTML(texto):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', texto)
    return cleantext

# Cria pasta para inserir as traduções
def criaPasta():
    if not os.path.exists(cwd + "\\translation\\" + versaoAtual): # se nao existir pasta criar
        os.makedirs(cwd + "\\translation\\" + versaoAtual)
    else:
        shutil.rmtree(cwd + "\\translation\\" + versaoAtual) # remove a pasta com todos os arquivos
        os.makedirs(cwd + "\\translation\\" + versaoAtual)    # criar novamente a pasta

# Busca os arquivos
def buscaArquivos(pasta, version):
    os.chdir(cwd + "\\" + pasta + "\\" + version)
    arquivos = glob.glob(arquivoTraducao)   # procurar nome parecidos
    return arquivos

# Conta dialogos
def contaDialogos():
    # Busca arquivos em ingles
    arquivos = buscaArquivos('versions', versaoAtual)

    #Lista os arquivos
    total = 0
    a = 0
    while a < len(arquivos): 
        # Abre o arquivo
        with open(arquivos[a], encoding="utf8") as f:
            data = json.load(f)
        total = total + len(data["strings"])
        a = a + 1
    return total

# Percentual de tradução
def percentualTraduzido(valor = 0, total = 0):
    result = (valor * 100) / total
    return result

# Retorna todos os textos revisados
def revisaoValue():
    # Busca arquivos em portugues
    arquivos = buscaArquivos('translation', versaoAnterior)
    dataLista = []
    # Busca todos os textos revisados na versão anterior
    i = 0
    while i < len(arquivos):
        with open(cwd + "\\translation\\" + versaoAnterior + "\\" + arquivos[i], encoding="utf8") as d:
            data = json.load(d)
        k = 0
        while k < len(data["strings"]):
            dataLista.append(data["strings"][k])    
            k = k + 1 
        i = i + 1
    # Retorna 
    return dataLista

# Busca texto em lista
def buscaTextoRevisado(keyTexto, lista):
    # time.sleep(0.1)
    i = 0
    while i < len(lista):
        if(lista[i]["Key"] == keyTexto):
            try:
                if(lista[i]["Key"] == "b47d60ef-037e-4d17-b454-47b90fcc3861"):
                    print("Recuperando texto revisado...")
                    return "Mutar: Esta trução foi desenvolvida como um desafio pessoal e apoiada pela comunidade do canal Mutar Club. Agradeço a todos os envolvidos no desenvolvimento, apoio, revisão e divulgação. Sua tradução foi revidada pela ultima vez no dia: " + str(datetime.datetime.now()) + ". Estaremos fazendo novas revisões, então fique por dentro se inscrevendo no canal Mutar Club. "
                else:
                    print("Recuperando texto revisado...")
                    return lista[i]["Value"]
            except:
                print("Chave de Revisão com problema!")
                return False
        i = i + 1
    return False


# Ler & Escrever arquivos
def lerEscrever(contDialogos, textoRevisado):
    # Cria a pasta
    criaPasta()

    # Busca arquivos em ingles
    arquivos = buscaArquivos('versions', versaoAtual)

    #Lista os arquivos
    a = 0
    countTotal = 0
    while a < len(arquivos): 
        # Abre o arquivo da versao atual
        with open(cwd + "\\versions\\" + versaoAtual + "\\" + arquivos[a], encoding="utf8") as f:
            data = json.load(f) 
            
        # Abrir os textos revisados e não revisados para tradução
        i = 0
        while i < len(data["strings"]):
            # Busca o texto dentro da ultima versão revisada
            textoRev = buscaTextoRevisado(data["strings"][i]["Key"], textoRevisado)
            # Se existir o texto apenas copia, caso contrario traduz o texto
            if(textoRev):
                data["strings"][i]["Value"] = textoRev
            else:
                data["strings"][i]["Value"] = traduzir(data["strings"][i]["Value"])
                
            print("%.2f" % percentualTraduzido(countTotal, contDialogos))
            countTotal = countTotal + 1
            i = i + 1
        
        # Escreve o arquivo
        with open(cwd + '\\translation\\' + versaoAtual  + '\\' + arquivos[a], 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        a = a + 1

print("##################################################################################")
print("## Tradutor Pathfinder: King Maker                                              ##")
print("## Criado por Mutar                                                             ##")
print("## YouTube: Mutar Club                                                          ##")
print("##                                                                              ##")
print("## Agradecimentos Especiais                                                     ##")
print("## DaftPunk - Por contribuir com partes do código                               ##")
print("## NightWolf - Por ajudar na divulgação da tradução                             ##")
print("## Insoneo - Por reunir as traduções existentes, revisar e postar no nexusmods  ##")
print("## Skywalker - Por ajudar o Insoneo com a tabela de textos.                     ##")
print("##                                                                              ##")
print("## Agradeço a todos do meu canal no youtube que me deram um feedback positivo e ##")
print("## tornaram esse sistema de tradução prossivel, vocês são GOD de mais!          ##")
print("##################################################################################")
print("Pasta da versão atual com arquivos em inglês ")
versaoAtual = input()
print("Pasta da versão anterior com arquivos em português ")
versaoAnterior = input()

print("##### -- Iniciando tradução -- #####")
textosRevisados = revisaoValue() # Pega todos os textos em pt da ultima versao
totalDialogos = contaDialogos() # Contagem dos textos da nova versão
lerEscrever(totalDialogos, textosRevisados) # Faz a tradução

