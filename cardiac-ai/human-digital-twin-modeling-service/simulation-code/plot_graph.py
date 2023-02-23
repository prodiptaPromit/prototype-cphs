import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns


def plot_graph(g, attention, ax, nodes_to_plot=None, nodes_labels=None,
               edges_to_plot=None, nodes_pos=None, nodes_colors=None,
               edge_colormap=plt.cm.Reds):
    if nodes_to_plot is None:
        nodes_to_plot = sorted(g.nodes())
    if edges_to_plot is None:
        assert isinstance(g, nx.DiGraph), 'Expected g to be an networkx.DiGraph' \
                                          'object, got {}.'.format(type(g))
        edges_to_plot = sorted(g.edges())
    nx.draw_networkx_edges(g, nodes_pos, edgelist=edges_to_plot,
                           edge_color=attention, edge_cmap=edge_colormap,
                           width=2, alpha=0.5, ax=ax, edge_vmin=0,
                           edge_vmax=1)

    if nodes_colors is None:
        nodes_colors = sns.color_palette("deep", max(nodes_labels) + 1)

    nx.draw_networkx_nodes(g, nodes_pos, nodelist=nodes_to_plot, ax=ax, node_size=30,
                           node_color=[nodes_colors[nodes_labels[v - 1]]
                                       for v in nodes_to_plot],
                           with_labels=False, alpha=0.9)
