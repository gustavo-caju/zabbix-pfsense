from re import sub

def getSwanConf(file_path):
    with open(file_path, 'r') as file:
        confFile = file.read()


    confFile = sub(r'#.*\n', '', confFile)     # remove comentario
    confFile = sub(r'^$', '', confFile)        # remove linhas em ranco
    confFile = sub(r'"', '\'', confFile)       # subtitui " por '
    confFile = sub(r'\s=\s', ':', confFile)    # remove o "
    confFile = sub(r'([\w\.\/|%=:,\'-]+):([\w\.\/|%=:,\'-]+)', r'"\1":"\2"', confFile)  # adiciona o "
    confFile = sub(r'([\w\.\/|%=:,\'-]+)\s{', r'"\1": {', confFile)    # inicio  de chave, adiciona {
    confFile = sub(r'}\s*\n\s*"', '},\n"', confFile)   # adiciona virgula
    confFile = sub(r'"\s*\n\s*"', '",\n"', confFile)   # adicionar virgula
    confFile = sub(r'^', '{', confFile)                # adiciona { no inicio do dicionario
    confFile = sub(r'}$\s*\n\s*', '}}', confFile)      # adicionar } ao final do dicionario
    # confFile = sub(r'con\d+_(\d+)', r'\1', confFile)  # adicionar } ao final do dicionario

    confFile = eval(confFile)
    del confFile['connections']['bypass']
    confFile = confFile.get('connections')
    swanList = []
    for k, v in confFile.items():
        swan = {}
        swan['ikeid'] = sub('con(\d+)',r'\1', k)
        swan['phases'] = []
        for key, value in v['children'].items():
            child = {}
            child['id'] = key
            child['local'] = value['local_ts']
            child['remote'] = value['remote_ts']
            swan['phases'].append(child)
        swanList.append(swan)
    return swanList
