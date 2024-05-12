import networkx as nx
from variables import rows, cols

def encodedMap_to_graph(rows, cols, mapa_code):
    '''
    This function receives the encoded map, and transforms it to a networkx graph.

    Parameters:
        rows(int): The number of rows the map has.
        cols(int): The number of columns the map has.
        mapa_code(string): The codified map as it's posted in the mqtt broker.
    
    Returns:
        G(Graph): A Graph class object containing the map.
    '''
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
    '''
    This function return the shortest path between two locations in the map (nodes in the graph).

    Parameters:
        Graph(Graph): A networkx Graph object.
        ini(int): Integer indicating the id of the initial node.
        fin(int): Integer indicating the if of the ending node.

    Returns:
        path(list): A list containing the nodes in the shortest path.
    '''
    return nx.dijkstra_path(Graph, ini, fin)

def path_to_movement(path,cols,rows):
    '''
    This function receives the list of nodes with the shortest path, and transform it to a list containing the corresponding movement between nodes.

    Parameters:
        path(List): A list containing the nodes id 
    
    Returns:
        movement(List): A list of movements codified as [up,down,left,right]
    '''
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
    '''
    This function receives a delivery order, the current position of the robot, and the map graph.
    It returns a list of movements the robot can understand to succesfully complete the delivery.

    Parameters:
        pick_pos (int): Integer indicating the node in which the robot has to pick the package.
        delivery_pos (int): Integer indicating the node in which the robot has to deliver the package.
        initial_pos (int): Integer indicating the node in which the robot is located.
    
    Returns:
        list[string]: Returns a list of strings. Those strings correspond to the diferent actions the robot should make in order to complete the delivery.
    '''
    to_pick = path_to_movement(path=dijkstra(Graph=graph,ini=initial_pos,fin=pick_pos),cols=cols,rows=rows)
    to_pick.append('pick')
    to_delivery = path_to_movement(path=dijkstra(Graph=graph,ini=pick_pos,fin=delivery_pos),cols=cols,rows=rows)
    to_delivery.append('drop')
    return to_pick+to_delivery