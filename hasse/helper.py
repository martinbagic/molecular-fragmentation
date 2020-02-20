import os

def PATH(s):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if isinstance(s, str):
        return os.path.join(base_dir, s)
    else:
        return os.path.join(base_dir, *s)
