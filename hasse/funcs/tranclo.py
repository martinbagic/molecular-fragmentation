def get_transitive_closure(poset):
    tc = {node: [] for node in poset.keys()}

    for start in poset.keys():
        for end in poset[start]:
            flag = False
            for mid in poset[start]:
                if end in poset[mid] and end != mid:
                    flag = True
                    break
            if not flag:
                tc[start].append(end)

    return tc
