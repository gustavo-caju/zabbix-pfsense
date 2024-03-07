

def getFormated(ipsecList, swanList):
    for p2 in [ipsec for ipsec in ipsecList if ipsec['phase'] == 2 ]:
        for swan in [s['phases'] for s in swanList if s['ikeid'] == p2['ikeid'] ]:
            for s in swan:
                if p2['con'] == s['id']:
                    p2['local'] = s['local']
                    p2['remote'] = s['remote']
    return ipsecList
