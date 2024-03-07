from xml.etree import ElementTree as ET

def getIpsecConf(xmlFile):
    xmlConf = ET.parse(xmlFile).getroot()
    ipsecList = []
    ipsec1 = getPhase1(xmlConf)
    ipsec2 = getPhase2(xmlConf)

    for p1 in ipsec1:
        ipsecList.append(p1)
        for p2 in ipsec2:
            if p1.get('ikeid') == p2.get('ikeid'):
                if p1.get('disabled'):
                    p2['disabled'] = True
                p2['descr'] = p1.get('descr')
                ipsecList.append(p2)
    return ipsecList

def interfaceName(xmlConf, phase):
    confFile = xmlConf.find("interfaces")
    for item in confFile:
        if item.tag == phase['interface']:
            phase['interface'] = str(item.findtext('if'))
            phase['local'] = str(item.findtext('ipaddr'))
            phase['alias'] = str(item.findtext('descr'))
def getPhase1(xmlConf):
    ipsecList = []
    confFile = xmlConf.findall('ipsec/phase1')
    for phase1 in confFile:
        phase = {'phase': 1, 'disabled': False}
        for item in phase1:
            if item.tag == 'ikeid':
                phase['ikeid'] = item.text
                phase['con'] = f'con{item.text}'
            if item.tag == 'disabled':
                phase['disabled'] = True
            if item.tag == 'descr':
                phase['descr'] = item.text
            if item.tag == 'remote-gateway':
                phase['remote'] = item.text
            if item.tag == 'interface':
                phase['interface'] = item.text
                interfaceName(xmlConf, phase)
        # if not phase.get('disabled'):
        ipsecList.append(phase)
    return ipsecList

def getPhase2(xmlConf):
    confFile = xmlConf.findall('ipsec/phase2')
    ipsec2List = []
    for phase2 in confFile:
        phase = {'phase': 2, 'disabled': False}
        for item in phase2:
            if item.tag == 'ikeid':
                phase['ikeid'] = item.text
                ikeid = item.text
            if item.tag == 'reqid':
                phase['con'] = f'con{ikeid}_{item.text}'
            # if item.tag == 'descr':
            #     phase['descr'] = item.text
            if item.tag == 'disabled':
                phase['disabled'] = True
        # if not phase.get('disabled'):
        ipsec2List.append(phase)
    return ipsec2List
