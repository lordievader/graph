"""Author:      Olivier van der Toorn <o.i.vandertoorn@utwente.nl>
Description:    Library for building graphs.
"""
import matplotlib.pyplot as plt
import networkx
from networkx.drawing.nx_agraph import graphviz_layout



class Graph():
    """Graph representation
    """
    defaults = {
        'value': 0,
        'color': 'green',
    }
    required_keys = ['value', 'color']

    def __init__(self, name, parent=None, attributes=None):
        """Graph representation.

        :param name: name of the root node
        :type name: str
        :param parent: (optional) reference to a parent Graph
        :type parent: Graph
        :param attributes: dictionary of node attributes
        :type attributes: dict
        """
        self.name = name
        self.parent = parent
        if attributes is None:
            self.attributes = {}

        else:
            self.attributes = attributes

        for key in self.required_keys:
            if key not in self.attributes:
                if key == 'color' and parent is not None:
                    value = parent.attributes[key]

                else:
                    value = self.defaults[key]

                self.attributes[key] = value

        self.children = []
        if self.parent is not None:
            self.parent.add_child(self)

        self.graph = networkx.DiGraph()

    def build(self):
        """Build the actual graph.
        """
        self.graph.clear()
        self.graph.add_node(self.name, **self.attributes)
        for child in self.children:
            child.build()
            self._add_node(child)

    def add_child(self, node):
        """Adds a child graph.

        :param node: node to add as child.
        :type node: graph
        """
        self.children.append(node)

    def _add_node(self, node):
        """(private) Add a subgraph to this graph.

        :param node: node to add as child.
        :type node: Graph
        """
        if 'value' in node.attributes:
            self.attributes['value'] += node.attributes['value']
            self.graph.nodes[self.name]['value'] += node.attributes['value']

        self.graph.add_nodes_from(node.graph.nodes())
        self.graph.add_edges_from(node.graph.edges())
        self.graph.add_edge(self.name, node.name)
        for name in node.graph.node:
            for item, value in node.graph.node[name].items():
                self.graph.node[name][item] = value

    def show(self, axis=None, figsize=(7, 5)):
        """Plot the graph.

        :param ax: (optional) reference to a matplotlib axis
        :type ax: matplotlib.ax
        """
        self.build()
        if axis is None:
            _, axis = plt.subplots(1, 1, figsize=figsize)

        pos = graphviz_layout(self.graph, prog='neato')
        node_labels = {
            name: f'{name}\n{label}' for name, label in
            networkx.get_node_attributes(self.graph, 'value').items()}
        colors = [networkx.get_node_attributes(self.graph, 'color')[name]
                  for name in pos]
        networkx.draw(
            self.graph, pos, ax=axis, node_shape='H',
            node_size=2000, node_color=colors, alpha=0.5)
        networkx.draw_networkx_labels(
            self.graph, pos, ax=axis, labels=node_labels)

        return axis
