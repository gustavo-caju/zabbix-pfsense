#/bin/bash
#
# 
# Script para testar os status da fase 1 ou fase 2
#
# Gustavo Sobral (Caju)
# sobrall.gustavo@gmail.com


# testa a fase 1
statusPhase1 () {
    IP="$1"                                                     # atribuo para IP o parametro passada na funcao
    STATUS=$(ipsec status | grep "$IP" | awk '{print $2}')      # faz uma filtragem para coletar a coluna da string onde tem a informaçao
    case $STATUS in
        "ESTABLISHED")
            echo -n 1
            break
            ;;
        "CONNECTING")
            echo -n 2
            break
            ;;
        *)
            echo -n 0
            break
            ;;
    esac
}

statusPhase2 () {
    CON="$1"                                            # tribuo para CON o parametro passada na funcao, a con da fase 2
    ipsec status $CON | grep "INSTALLED" 2> /dev/null
    if [ $? -eq 0 ] ; then                              # valida a execução do comando anterior, se econtrou a string INSTALLED
        echo -n 1                                       # retorna 1, a fase 2 está UP
    else
        echo -n 0
    fi
}



tuneltest () {
    OPT="$1"
    case "$OPT" in
        1)
            statusPhase1 "$2"
            break
            ;;
        2)
            statusPhase2 "$2"
            break
            ;;
        *)
            echo "error"
            break
            ;;
    esac
}


# chama a funcao pasando os dados ou da fase 1 ou da fase 2
tuneltest "$1" "$2"


# exemplo de chamado pelo zabbix
#  $ ipsecstatus.sh 1 233.252.0.3
#  $ ipsecstatus.sh 2 con10001  
#
#   para fase 1: passar "1" e o IP (rid)
#   para fase 2: passar "2" e a con da fase 2
