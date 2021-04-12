"""Author:      Olivier van der Toorn <o.i.vandertoorn@utwente.nl>
Description:    Library for building graphs.
"""
import logging
import matplotlib.pyplot as plt
import numpy
import networkx
from networkx.drawing.nx_agraph import graphviz_layout


class Graph():
    """Graph representation
    """
    defaults = {
        'value': 0,
        'percent': 0,
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
            value = node.attributes['value']
            self.attributes['value'] += value
            self.graph.nodes()[self.name]['value'] += value

        if 'percent' in node.attributes:
            percent = node.attributes['percent']
            self.attributes['percent'] += percent
            self.graph.nodes()[self.name]['percent'] += percent

        self.graph.add_nodes_from(node.graph.nodes())
        self.graph.add_edges_from(node.graph.edges())
        self.graph.add_edge(self.name, node.name)
        for name in node.graph.nodes():
            for item, value in node.graph.nodes()[name].items():
                self.graph.nodes()[name][item] = value

    def show(self, axis=None, figsize=(7, 5), dynamic_size=False):
        """Plot the graph.
        Dynamic size can be a boolean or one of 'lin', 'exp', or 'log'.

        :param ax: (optional) reference to a matplotlib axis
        :type ax: matplotlib.ax
        :param figsize: (optional) figure size
        :type figsize: tuple (width, height)
        :param dynamic_size: let the size be dependend on the percentage
        :type dynamic_size: boolean/str
        :return: matplotlib axis
        """
        self.build()
        if axis is None:
            _, axis = plt.subplots(1, 1, figsize=figsize)

        pos = graphviz_layout(self.graph, prog='neato')
        values = networkx.get_node_attributes(self.graph, 'value')
        percentages = networkx.get_node_attributes(self.graph, 'percent')
        node_labels = {}
        for name, value in values.items():
            percent = percentages[name]
            node_labels[name] = f'{name}\n{value}\n{percent:5.2f}%'

        base_size = 2000
        if dynamic_size is not False:
            node_sizes = []
            for name in pos.keys():
                percent = percentages[name]
                if dynamic_size == 'exp':
                    node_size = base_size * ((percent * percent) / 10000)

                elif dynamic_size == 'log':
                    node_size = base_size * (0.5 * numpy.log10(percent))

                else:
                    node_size = base_size * (percent / 100)

                node_sizes.append(node_size)

        else:
            node_sizes = base_size

        colors = [networkx.get_node_attributes(self.graph, 'color')[name]
                  for name in pos]
        networkx.draw(
            self.graph, pos, ax=axis, node_shape='o',
            node_size=node_sizes, node_color=colors, alpha=0.5)
        networkx.draw_networkx_labels(
            self.graph, pos, ax=axis, labels=node_labels)
        return axis
