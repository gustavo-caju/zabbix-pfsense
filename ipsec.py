'''
Gustavo Sobral (Caju)
sobrall.gustavo@gmail.com
v 1.0

Este script retornar um json das configurações do IPSEC
'''

from xml.etree import ElementTree as ET
from json import dumps
import re
from sys import exit

# Funcao para coletar as CONs do arquivo de configuração do IPSEC
def obtemCon():
    with open('/var/etc/ipsec/ipsec.conf', 'r') as ipconf:          # abre arquivo de configuração
        conre = re.compile(r'.*conn\s(con[\d]+)$')
        lidre = re.compile(r'.*leftid = ([\w.\d/]+)$')
        ridre = re.compile(r'.*rightid = ([\w.\d/]+)$')
        leftnetre = re.compile(r'\sleftsubnet = ([\w.\d/|]+)$')
        rightnetre = re.compile(r'\srightsubnet = ([\w.,\d/|]+)$')  # regex para extratir palavras chaves do arquivo de configuração
        dicio = {} # inicia um dicionario
        lista = [] # inicia uma lista
        for line in ipconf.readlines():                              # incia a leitura de cada linha
            con = conre.search(line)                                 # tenta capturar o nome da con
            if con: dicio['con'] = con.group(1); continue            # se localizou a con é adicionado a um dicionario

            lid = lidre.search(line)
            if lid: dicio['lid']=lid.group(1); continue              # se localizou o left id é adicionado a um dicionario

            rid = ridre.search(line)
            if rid: dicio['rid'] = rid.group(1); continue            # se localizou o right id é adicionado a um dicionario

            rnet = rightnetre.search(line)
            if rnet: dicio['rnet'] = rnet.group(1); continue         # se localizou o left subnet é adicionado a um dicionario

            lnet = leftnetre.search(line)  
            if lnet:                                                 # se localizou left subnet é adicionado a um dicionario
                dicio['lnet'] = lnet.group(1)                        # o script segue a leitura das linhas no sntido de cima para baixo
                lista.append(dicio)                                  # left subnet é um dos ultimos no arquivo de configuracao
                dicio = {}                                           # encontrando a ultima linha do bloco adiciono em uma lista e zero o dicionario
    return lista

# funcao para extratir a configuração da fase1 nas configuracoes do pfsende
def phase1():
    ipsecdados=[] 
    confFile = ET.parse('/cf/conf/config.xml').getroot()    # necessário para acessar o arquivo xml
    confFile = confFile.findall('ipsec/phase1')             # filtra por ipsec phase1 no arquivo xml
    for phase1 in confFile:                                 # loop para cada entrada fase 1 do xml
        dicio = {}                                          # inicia o dicionario para cada entrada do ipesec no xml
        dicio['phase'] = 1                                  # adiciona um item como phase 1, usado como tag no zabbix
        for item in phase1:                                 # para cada item na fase 1 no xml
            if item.tag in ('ikeid', 'iketype', 'remote-gateway', 'interface', 'descr', 'disabled'):  # filtro para somente algumas tags
                if item.tag == 'remote-gateway':
                    dicio['rid'] = item.text                # adiciona o right id (IP) da IPSEC, aqui troco o remote-gateway por 'rid', apenas troca de nome
                else:
                    dicio[item.tag] = item.text             # adiciona todas as tags encontradas ao dicionario
        if not dicio.get('disabled'):                       # condição para não coletar as VPNs desabilitadas
            ipsecdados.append(dicio)                        # ao final do loop de cada phase1 adiciona a uma lista
    return ipsecdados


# funcao para retornar os dados coletados de forma mais organizada para o zabbix
def ipconf():
    newList = []
    newDict = {}
    for p1 in phase1():                             # pego o retorno da fase1 e faço o loop para cada entrada
        for con in obtemCon():                      # pego o retorno das Cons e faço o loop para cada entrada, aqui é organizado a fase2      
            newDict = {}                            # zero o dicionario para nao gerar entradas repetidas
            if con.get('rid') == p1.get('rid'):     # se rightid da con e da fase1 forem as mesmas, adiciono em um mesmo dicionario
                newDict['phase'] = 2                # como é a primeira entra do novo dicionario coloco a tag da fase 2, sera usado no zabbix
                newDict['ikeid'] = p1.get('ikeid')  # uso o mesmo ikeid do arquivo de configuraçao do pfsense, usado para fltragens no zabbix
                newDict['descr'] = p1.get('descr')  # uso o mesmo nome dado no arquivo de configuração do pfsense
                p1['lid'] = con.get('lid')          # na leitura fase1 da configuracao do pfsense nao tem o IP do Left ID, entao adiciono aqui
                for i in con:                       # obtemCon() retorna uma lista de dicionarios, então o loop percorre cada item do dicionario
                    newDict[i] = con[i]             # cada entrada das CONs são adicionadas a fase2 do novo dicionario
                newList.append(newDict)             # ao final de cada loop da obtemCon adiciono a lista nova
        newList.append(p1)                          # ao final de cada loop da Pshase1 adiciono a lista nova
    return (newList)                              # retorno a nova lista, com as fases 1 e 2 organizadas

if __name__ == "__main__":
    exit(dumps(ipconf()))                           # para o discovery do zabbix envio como um json



'''
exemplo de retorno

[
  {
    "phase": 2,
    "ikeid": "3",
    "descr": "CLIENT",
    "lnet": "10.10.0.0/24",
    "con": "con3000",
    "lid": "203.0.113.1",
    "rid": "233.252.0.3",
    "rnet": "192.168.0.0/24"
  },
  {
    "phase": 2,
    "ikeid": "3",
    "descr": "CLIENT",
    "lnet": "10.10.10.0/24|10.10.0.0/24",
    "con": "con3001",
    "lid": "203.0.113.1",
    "rid": "233.252.0.3",
    "rnet": "192.168.0.0/24"
  },
  {
    "phase": 2,
    "ikeid": "3",
    "descr": "CLIENT",
    "lnet": "10.10.30.0/24|10.10.0.0/24",
    "con": "con3002",
    "lid": "203.0.113.1",
    "rid": "233.252.0.3",
    "rnet": "192.168.0.0/24"
  },
  {
    "phase": 2,
    "ikeid": "3",
    "descr": "CLIENT",
    "lnet": "10.10.30.0/24",
    "con": "con3003",
    "lid": "203.0.113.1",
    "rid": "233.252.0.3",
    "rnet": "192.168.0.0/24"
  },
  {
    "phase": 1,
    "ikeid": "3",
    "iketype": "ikev1",
    "interface": "opt2",
    "rid": "233.252.0.3",
    "descr": "AMIL",
    "lid": "203.0.113.1"
  }
  ]

'''