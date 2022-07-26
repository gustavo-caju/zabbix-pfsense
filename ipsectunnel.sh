#/bin/bash
#
#
# Script para coletar o tráfego da fase2
#
# Gustavo Sobral (Caju)
# sobrall.gustavo@gmail.com


tunnelTraffic () {
    CON=$(ipsec statusall "$1" | grep "bytes") 
    if [ $? -eq 0 ] ; then                          # teste para validar se a fase 2 está UP para encontrar 
        case $2 in
            "in")
                IN=$(echo -n $CON | awk '{print $3}')  # coleta a coluna 3
                printf "$IN"
                break
                ;;
            "out")
                IN=$(echo -n $CON | awk '{print $9}')  # coleta a coluna 4
                printf "$IN"
                break
                ;;
            *)
                printf "error"
                ;;
        esac
    else
        echo -n 0
    fi

tunnelTraffic $1 $2


# exemplo de chamada do script
# $ ipsectunel.sh con10001 in
# $ ipsectunel.sh con10001 out
#
#
#
#
#
