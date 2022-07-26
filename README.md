# Monitoramento do IPSEC no pfSense
Projeto para monitoramento dos tuneis de fase 1 e 2 do IPSec no pfSense.
Os testes realizados fora no pfSense 2.4.5 e zabbix 6.0
Pretendo em breve atualizar para as versões mais novas do pfSense
Desde já agrdeço qualquer contribuição nesse projeto.

caso queira entre em contato comigo por email: sobrall.gustavo@gmail.com

# Como Funciona?
Basicamente o zabbix solicita ao zabbix agent no pfsense as fases 1 e 2. Que virá em formatado json.
No zabbix iniciaram a descoberta por item dependente.
Será criado itens para cada fase 1 e fase2. A fase 2 será atrelada a cada nome da fase 1

será monitorado da fase 1 a disponibilidade por ping e latência e o status de comunicação da fase 1
na fase 2 será monitorado o status de comunicação e tráfego de entrada e saída do tunel criado. 

# Instalação
- Copiar arquivos:  
  Deverá ser copiado os arquivos abaixo para a pasta de instalação do zabbix no pfsense, geralmente na pasta "**/usr/local/etc/zabbix52/zabbix_agentd.conf.d/**"
  "*ipsec.py*"  
  "*ipsecstatus.sh*"  
  "*ipsectraffic.sh*"  
     
  *Neste projeto foi utilizado a versão do zabbix Agent 5.2*


- Configurar o UserParameter no pfSense:
  * UserParameter=pfsense.ipsec.get, /usr/local/bin/python3.7 /usr/local/etc/zabbix52/zabbix_agentd.conf.d/ipsec.py $1
  * UserParameter=pfsense.ipsec.status[*], /usr/local/etc/zabbix52/zabbix_agentd.conf.d/ipsecstatus.sh $1 $2
  * UserParameter=pfsense.ipsec.traffic[*], /usr/local/etc/zabbix52/zabbix_agentd.conf.d/ipsectraffic.sh $1 $2

  obs.: possivelmente algumas versões do pfsense ainda utilizem o python 2, neste apenas colocar o caminho do executável do python 2


- Alterar dono dos arquivos:
 ```
  # chown :zabbix /usr/local/etc/zabbix52/zabbix_agentd.conf.d/ipsec* 
 ```

- Reiniciar o restart do serviço do zabbix no pfSense


- Por fim, importar o template para o zabbix.


# Observações:
  Ao utilizar NAT T no tunel da fase 2, algumas CONs podem não ter tráfego nem mesmo subir no status do ipsec.
  Ainda não encontrei uma solução para isto.

