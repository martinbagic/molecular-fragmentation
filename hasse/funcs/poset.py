def get_poset(genfunc, roots):
    stack = roots[:]
    poset = dict()

    while stack:
        pop = stack.pop()
        poset[pop] = set()
        for n in poset:
            if pop == n:
                continue
            child = genfunc(pop, n)
            # if self.plot_images:
            #     child = self.get_canonical(child)
            #     if '.' in child:  # FIX THIS
            #         print(child)
            #         child = max(child.split('.'),
            #                     key=lambda x: atom_count(x))
            if child != n:
                poset[n].add(child)
            if child != pop:
                poset[pop].add(child)

            if child not in poset and child not in stack:
                stack.append(child)

    return poset
