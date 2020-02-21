import helper
from . import hack
import graphviz

def get_digraph(g, roots, mode):
    conf = helper.DIGRAPH_SETTINGS

    # configuration
    graph = graphviz.Digraph()
    graph.format = conf['format']
    graph.edge_attr.update(**conf['edge_attr'])

    # styling
    if mode == 'mcs':
        add_images(graph, g, roots)

    elif mode == 'gcd':
        g = {str(k): [str(x) for x in v] for k, v in g.items()}
        roots = [str(root) for root in roots]
        add_text(graph, roots)

    else:
        add_text(graph, roots)

    # add nodes and edges
    for node0, nodes1 in g.items():
        for node1 in nodes1:
            graph.edge(node0, node1)

    return graph


def add_text(graph, roots):
    for root in roots:
        graph.node(
            root,
            label=root,
            fillcolor='gold',
            style='filled',
        )


def add_images(graph, g, roots):

    def legalize(name):
        s1 = '<>:"/\|?*()'
        s2 = 'üéâäàåçêëèïîì'
        replacements = dict(zip(s1, s2))
        for a, b in replacements.items():
            name = name.replace(a, b)
        return name

    for node in g.keys():
        if node:
            filename = f'{legalize(node)}.svg'

            print(node)
            print(helper.PATH(['plots', filename]))

            hack.draw_smiles(
                smiles=node,
                path=helper.PATH(['plots', filename]),
            )
        else:
            filename = 'empty.svg'

        graph.node(
            node,
            label='',
            image=filename,
            shape='rect' if node in roots else 'none',
        )
