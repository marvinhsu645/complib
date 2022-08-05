
class Vertex:
    def __init__(self, key, vertex_type, value=None):        
        self.id = key
        self.type = vertex_type
        self.value = value
        self.neighbors = []
    def add_neighbor(self, nbr):
        self.neighbors.append(nbr)
    def __str__(self):
        # return f"{str(self.id)} connected to: {str([x.id for x in self.neighbors])}"
        return f"{str(self.id)}"
    def get_neighbors(self):
        return self.neighbors
    def get_id(self):
        return self.id
        

class TripartiteGraph:
    def __init__(self):
        self.vertices = {}

    def __iter__(self):
        return iter(self.vertices.values())

    def add_vertex(self, node, type):
        # self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node, type)
        self.vertices[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def add_edge(self, frm, to):
        if frm not in self.vertices:
            self.add_vertex(frm)
        if to not in self.vertices:
            self.add_vertex(to)

        self.vertices[frm].add_neighbor(self.vertices[to])
        self.vertices[to].add_neighbor(self.vertices[frm])

    def add_edge(self, n, c, p):
        self.vertices[n].add_neighbor(self.vertices[p])
        self.vertices[p].add_neighbor(self.vertices[n])
        self.vertices[c].add_neighbor(self.vertices[p])
        self.vertices[p].add_neighbor(self.vertices[c])

    def get_vertices(self):
        return self.vertices.keys()

    def get_comp_neighbor(self, pin):
        for i in self.vertices[pin].neighbors:
            if i.type == 'c':
                return i
        return None

def getSchematicGraph():
    g = TripartiteGraph()
    g.add_vertex('#PWR1', 'c')
    g.add_vertex('#PWR2', 'c')
    g.add_vertex('C1', 'c')
    g.add_vertex('C2', 'c')
    g.add_vertex('RA', 'c')
    g.add_vertex('RB', 'c')
    g.add_vertex('NE555', 'c')
    g.add_vertex('#PWR1_1', 'p')
    g.add_vertex('#PWR2_1', 'p')
    g.add_vertex('NE555_1', 'p')
    g.add_vertex('NE555_2', 'p')
    g.add_vertex('NE555_4', 'p')
    g.add_vertex('NE555_5', 'p')
    g.add_vertex('NE555_6', 'p')
    g.add_vertex('NE555_7', 'p')
    g.add_vertex('NE555_8', 'p')
    g.add_vertex('C1_1', 'p')
    g.add_vertex('C1_2', 'p')
    g.add_vertex('C2_1', 'p')
    g.add_vertex('C2_2', 'p')
    g.add_vertex('RA_1', 'p')
    g.add_vertex('RA_2', 'p')
    g.add_vertex('RB_1', 'p')
    g.add_vertex('RB_2', 'p')
    g.add_vertex('N1', 'n')
    g.add_vertex('N2', 'n')
    g.add_vertex('N3', 'n')
    g.add_vertex('N4', 'n')
    g.add_vertex('N5', 'n')

    g.add_edge('N1', 'NE555', 'NE555_2')
    g.add_edge('N1', 'NE555', 'NE555_6')
    g.add_edge('N1', 'RB', 'RB_1')
    g.add_edge('N1', 'C1', 'C1_1')
    g.add_edge('N2', 'NE555', 'NE555_4')
    g.add_edge('N2', 'NE555', 'NE555_8')
    g.add_edge('N2', 'RA', 'RA_2')
    g.add_edge('N2', '#PWR2', '#PWR2_1')
    g.add_edge('N3', 'NE555', 'NE555_7')
    g.add_edge('N3', 'RA', 'RA_1')
    g.add_edge('N3', 'RB', 'RB_2')
    g.add_edge('N4', 'C1', 'C1_2')
    g.add_edge('N4', 'C2', 'C2_2')
    g.add_edge('N4', 'NE555', 'NE555_1')
    g.add_edge('N4', '#PWR1', '#PWR1_1')
    g.add_edge('N5', 'NE555', 'NE555_5')
    g.add_edge('N5', 'C2', 'C2_1')
    # for i in g:
    #     print(i)
    return g

    
def getPatchGraph():
    g = TripartiteGraph()
    g.add_vertex('#PWR1', 'c')
    g.add_vertex('#PWR2', 'c')
    g.add_vertex('C1', 'c')
    g.add_vertex('C2', 'c')
    g.add_vertex('R1', 'c')
    g.add_vertex('R2', 'c')
    g.add_vertex('R3', 'c')
    g.add_vertex('R4', 'c')
    g.add_vertex('NE555V', 'c')
    g.add_vertex('LED1', 'c')
    g.add_vertex('LED2', 'c')
    g.add_vertex('#PWR1_1', 'p')
    g.add_vertex('#PWR2_1', 'p')
    g.add_vertex('NE555V_1', 'p')
    g.add_vertex('NE555V_2', 'p')
    g.add_vertex('NE555V_3', 'p')
    g.add_vertex('NE555V_4', 'p')
    g.add_vertex('NE555V_5', 'p')
    g.add_vertex('NE555V_6', 'p')
    g.add_vertex('NE555V_7', 'p')
    g.add_vertex('NE555V_8', 'p')
    g.add_vertex('C1_1', 'p')
    g.add_vertex('C1_2', 'p')
    g.add_vertex('C2_1', 'p')
    g.add_vertex('C2_2', 'p')
    g.add_vertex('R1_1', 'p')
    g.add_vertex('R1_2', 'p')
    g.add_vertex('R2_1', 'p')
    g.add_vertex('R2_2', 'p')
    g.add_vertex('R3_1', 'p')
    g.add_vertex('R3_2', 'p')
    g.add_vertex('R4_1', 'p')
    g.add_vertex('R4_2', 'p')
    g.add_vertex('LED1_1', 'p')
    g.add_vertex('LED2_1', 'p')
    g.add_vertex('LED1_2', 'p')
    g.add_vertex('LED2_2', 'p')
    g.add_vertex('N1', 'n')
    g.add_vertex('N2', 'n')
    g.add_vertex('N3', 'n')
    g.add_vertex('N4', 'n')
    g.add_vertex('N5', 'n')
    g.add_vertex('N6', 'n')
    g.add_vertex('N7', 'n')
    g.add_vertex('N8', 'n')

    g.add_edge('N1', 'NE555V', 'NE555V_7')
    g.add_edge('N1', 'R1', 'R1_2')
    g.add_edge('N1', 'R2', 'R2_1')

    g.add_edge('N2', 'NE555V', 'NE555V_2')
    g.add_edge('N2', 'NE555V', 'NE555V_6')
    g.add_edge('N2', 'R2', 'R2_2')
    g.add_edge('N2', 'C1', 'C1_1')

    g.add_edge('N3', 'C1', 'C1_2')
    g.add_edge('N3', 'NE555V', 'NE555V_1')
    g.add_edge('N3', 'C2', 'C2_2')
    g.add_edge('N3', 'LED2', 'LED2_2')
    g.add_edge('N3', '#PWR1', '#PWR1_1')

    g.add_edge('N4', 'R1', 'R1_1')
    g.add_edge('N4', 'NE555V', 'NE555V_8')
    g.add_edge('N4', 'NE555V', 'NE555V_4')
    g.add_edge('N4', 'R3', 'R3_1')
    g.add_edge('N4', '#PWR2', '#PWR2_1')

    g.add_edge('N5', 'NE555V', 'NE555V_3')
    g.add_edge('N5', 'LED1', 'LED1_2')
    g.add_edge('N5', 'R4', 'R4_1')
    
    g.add_edge('N6', 'R3', 'R3_2')
    g.add_edge('N6', 'LED1', 'LED1_1')
    
    g.add_edge('N7', 'R4', 'R4_2')
    g.add_edge('N7', 'LED2', 'LED2_1')
    
    g.add_edge('N8', 'NE555V', 'NE555V_5')
    g.add_edge('N8', 'C2', 'C2_1')
    # for i in g:
    #     print(i)
    return g

if __name__=="__main__":
    # getPatchGraph()
    # getSchematicGraph()
    print('test')