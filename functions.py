import networkx as nx
from variables import rows, cols

def encodedMap_to_graph(rows, cols, mapa_code):
    procesed = [mapa_code[i:i+2] for i in range(0, len(mapa_code), 2)]
    G = nx.Graph()
    G.add_nodes_from([i for i in range(len(procesed))])
    
    for i in range(len(procesed)):
        row = int(i/cols)
        col = i%cols
        c_arriba = ["02","03","06","07","08","10","11"]
        c_abajo = ["02","04","05","08","09","10","11"]
        c_derecha = ["01","03","04","07","08","09","11"]
        c_izquierda = ["01","05","06","07","09","10","11"]
        if procesed[i] in c_arriba:
            if row-1 >= 0:
                node = (row-1)*cols+col
                if procesed[node] != "00" and procesed[node] in c_abajo:
                    G.add_edge(i, node)
        if procesed[i] in c_abajo:
            if row+1 < rows:
                node = (row+1)*cols+col
                if procesed[node] != "00" and procesed[node] in c_arriba:
                    G.add_edge(i, node)
        if procesed[i] in c_derecha:
            if col+1 < cols:
                node = (row)*cols+col+1
                if procesed[node] != "00" and procesed[node] in c_izquierda:
                    G.add_edge(i, node)
        if procesed[i] in c_izquierda:
            if col-1 >= 0:
                node = (row)*cols+col-1
                if procesed[node] != "00" and procesed[node] in c_derecha:
                    G.add_edge(i, node)
    return G

def dijkstra(Graph, ini, fin):
    return nx.dijkstra_path(Graph, ini, fin)

def path_to_movement(path,cols,rows):
    res = []
    for i in range(len(path)-1):
        
        dif = path[i]-path[i+1]
        if dif==5:
            pass
        match dif:
            case 1:
                res.append('left')
            case -1:
                res.append('right')
            case 5:
                res.append('up')
            case _:
                res.append('down')
    return res

def delivery2movement(pick_pos,delivery_pos,initial_pos,graph):
    to_pick = path_to_movement(path=dijkstra(Graph=graph,ini=initial_pos,fin=pick_pos),cols=cols,rows=rows)
    to_pick.append('pick')
    to_delivery = path_to_movement(path=dijkstra(Graph=graph,ini=pick_pos,fin=delivery_pos),cols=cols,rows=rows)
    to_delivery.append('drop')
    return to_pick+to_delivery