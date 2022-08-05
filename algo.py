# C = {"#PWR1", "#PWR2", "C1", "C2", "RA", "RB", "NE555"}
# P = {"#PWR1_1", "PWR2_1", "NE555_1", "NE555_2", "NE555_4", "NE555_5", "NE555_6", "NE555_7", "NE555_8",
#              "C1_1", "C1_2", "C2_1", "C2_2", "RA_1", "RA_2", "RB_1", "RB_2"}
# N = {"N1", "N2", "N3", "N4", "N5"}
#
# ##a tripartite graph##
# netRepr = {"N1":{("NE555", "NE555_7"), ("R1", "R1_2"), ("R2", "R2_1")},
#            "N2":{("NE555", "NE555_2"), ("NE555", "NE555_6"), ("R2", "R2_2"), ("C1", "C1_1")}}

from tripartite_graph import *

def getTagset(name):
    if name == '#PWR1' or name == '#PWR2':
        return "'Power'"
    elif name == 'C1' or name == 'C2':
        return "'C'"
    elif name == 'RA' or name == 'RB' or name == 'R1' or name == 'R2' or name == 'R3' or name == 'R4':
        return "'R'"
    elif name == 'NE555' or name == 'NE555V':
        return "'Timer'"
    elif name == 'LED1' or name == 'LED2':
        return "'LED'"
def getPinNum(pin):
    return pin.split('_')[-1]


# 取得netlist graph
def NetlistExtraction(netlist):
    if netlist == "Schematic":
        return getSchematicGraph()
    elif netlist == "Patches":
        return getPatchGraph()

# 前處理
def ComponentPreprocessing(tripartite_graph):
    result_graph = TripartiteGraph()
    for v in tripartite_graph.vertices.values():
        if v.type == 'c':
            key_name = f'{v.id}:{{{getTagset(v.id)}}}'
            v.id = key_name
            result_graph.vertices[key_name] = v
        elif v.type == 'p':
            key_name = f'{v.id}:{{{getPinNum(v.id)}}}'
            v.id = key_name
            result_graph.vertices[key_name] = v
        elif v.type == 'n':
            result_graph.vertices[v.id] = v
    return result_graph

# ALGO
# targetGraph: patchgraph, matchingGraph: schematic
def AlgoProcedure(targetGraph, matchingGraph):
    target_visited = {}
    matching_visited = {}
    target_net_dict = {}
    matching_net_dict = {}
    for i, v in targetGraph.vertices.items():
        if v.type == 'n':
            target_net_dict[i] = targetGraph.vertices[i]
        else:
            target_visited[i] = False
    for i, v in matchingGraph.vertices.items():
        if v.type == 'n':
            matching_net_dict[i] = matchingGraph.vertices[i]
        else:
            matching_visited[i] = False
    
    # schematic 的 net graph 去跑
    for net_id, net_node in target_net_dict.items():
        neighbor_comps = []
        # 每一個 net 的 neighbor (pin)
        for pin_node in net_node.get_neighbors():
            # 再去找 pin 的 neighbor (comp)
            neighbor_comps.append(targetGraph.get_comp_neighbor(pin_node.id))
            # print(f'nei: {targetGraph.get_comp_neighbors(nei)}')
        for comp in neighbor_comps:
            print(f'{net_id}\'s neighbors: {comp}')

# 檢查有沒有patch
def NetTraversal(mainGraph, subGraphs):
    # preprocessingMainGraph = ComponentPreprocessing(mainGraph)
    # preprocessingSubGraphs = []
    resultPatch = []
    # for subGraph in subGraphs:
    #     preprocessingSubGraphs.append(ComponentPreprocessing(subGraph))

    for psg in subGraphs:
        if AlgoProcedure(psg, mainGraph):
            # resultPatch.append(subGraphs[preprocessingSubGraphs.index(psg)])
            resultPatch.append(subGraphs.index(psg))

    return resultPatch


# 合併Graph
def MergeGraphs(sourceGraph, targeGraph):
    pass

# 1. NetlistExtraction
# 2. PatchDetection
# 3. MergeGraphs


def PatchDetection(schematic, patches):
    # schematic = "(Components(comp)..."
    # patches = ["(...)", "(...)"]
    
    pSchematicGraph = ComponentPreprocessing(schematic)
    pSubGraphs = []
    for patch in patches:
        pSubGraphs.append(ComponentPreprocessing(patch))

    # for v in schematicGraph:
    #     print(f'g.vertices[{v.get_id()}]={schematicGraph.vertices[v.get_id()]}')
    # for v in patchGraphs[0]:
    #     print(f'g.vertices[{v.get_id()}]={patchGraphs[0].vertices[v.get_id()]}')


    matchedPatches = NetTraversal(pSchematicGraph, pSubGraphs)

    if matchedPatches:
        schematic = MergeGraphs(schematic, matchedPatches)

    return schematic


if __name__ == '__main__':
    schematicGraph = NetlistExtraction("Schematic")
    patchGraphs = []
    # for patch in patches:
    patchGraphs.append(NetlistExtraction("Patches"))
    PatchDetection(schematicGraph, patchGraphs)



    
# c = {"#PWR1:{'Power'}", "#PWR2:{'Power'}", "C1:{'C'}", "C2:{'C'}", "RA:{'R'}", "RB:{'R'}", "NE555:{'Timer'}"}
# p = {"#PWR1_1:1", "PWR2_1:1", "NE555_1:1", "NE555_2:2", "NE555_4:4", "NE555_5:5", "NE555_6:6", "NE555_7:7", "NE555_8:8",
#              "C1_1:1", "C1_2:2", "C2_1:1", "C2_2:2", "RA_1:1", "RA_2:2", "RB_1:1", "RB_2:2"}
# n = {"N1", "N2", "N3", "N4", "N5"}
#
# ## a tripartite graph ##
# netRepr = {"N1":{("NE555:{'Timer'}", "NE555_7"), ("RA:{'R'}", "RA_2"), ("RB:{'R'}", "RB_1")},
#            "N2":{("NE555:{'Timer'}", "NE555_2"), ("NE555:{'Timer'}", "NE555_6"), ("RB{:'R'}", "RB_2"), ("C1:{'C'}", "C1_1")}}
