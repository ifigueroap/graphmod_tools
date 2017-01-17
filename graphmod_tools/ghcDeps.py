from pydotplus import *
from fnmatch import fnmatch

def flatten_node_labels(graph, prefix):
    nodes = {}
    for node in graph.get_nodes():
        noquotes_node_label = node.get_label()[1:-1]
        if not prefix:
            node.set_label("%s" % noquotes_node_label)
        else:
            node.set_label("%s.%s" % (prefix, noquotes_node_label))
        nodes[node.get_name()] = node

    for subgraph in graph.get_subgraphs():
        noquotes_subgraph_label = subgraph.get_label()[1:-1]
        if not prefix:
            nodes.update(flatten_node_labels(subgraph, "%s" % noquotes_subgraph_label))
        else:
            nodes.update(flatten_node_labels(subgraph, "%s.%s" % (prefix, noquotes_subgraph_label)))

    return nodes


def get_component_dirs(compilerPath):
    #return [os.path.relpath(x, compilerPath) for x in filter(os.path.isdir, [os.path.join(compilerPath, f) for f in os.listdir(compilerPath)])]
    return filter(os.path.isdir, [os.path.join(compilerPath, f) for f in os.listdir(compilerPath)])


def get_component_modules(componentPath, pattern = "*.hs"):
    modules = []
    for path, subdirs, files in os.walk(componentPath):
        for name in files:
            if fnmatch(name, pattern):
                 module_path = os.path.join(os.path.relpath(path, componentPath), name)
                 module_str = module_path.replace("build.", "").replace("./", "").replace("/", ".").replace(".hs", "")
                 module_str =  ".".join(filter(lambda x: x[0].isupper(), module_str.split('.')))
                 modules.append(module_str)

    return modules


def get_normalized_nodes_and_edges(dotfile, compilerRootPath):
   graph = graphviz.graph_from_dot_file(dotfile)
   flatnodes = flatten_node_labels(graph, "")
   flatnodes_inv = {v.get_label(): k for k, v in flatnodes.items()}

   component_modules = []
   for component in get_component_dirs(compilerRootPath):
        for module in get_component_modules(component):
             component_modules.append((os.path.relpath(component, compilerRootPath), flatnodes[flatnodes_inv[module]]))

   normalized_nodes = {}
   for component, node in component_modules:
       node.set_label(component + "." + node.get_label())
       normalized_nodes[node.get_name()] = node

   return (normalized_nodes, graph.get_edges())


def get_static_dependencies(dotfile, compilerRootPath):
   normalized_nodes, edges = get_normalized_nodes_and_edges(dotfile, compilerRootPath)
   return [(normalized_nodes[e.get_source()], normalized_nodes[e.get_destination()]) for e in edges]


def print_static_dependencies_rsf(static_deps):
   print("\n".join(["uses %s %s" % (src.get_label(), dst.get_label()) for (src, dst) in static_deps]))
   
