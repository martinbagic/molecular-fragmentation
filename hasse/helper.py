import os

def PATH(s):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if isinstance(s, str):
        return os.path.join(base_dir, s)
    else:
        return os.path.join(base_dir, *s)

MCS_PATH = PATH(['..','mcs-cliquer-1.0.0','mcs','mcs'])

DIGRAPH_SETTINGS = {
    'edge_attr': {
        'arrowhead': 'vee',
        'arrowsize': '0.5',
        'splines': 'curved',
    },
    'format': 'svg',

}

