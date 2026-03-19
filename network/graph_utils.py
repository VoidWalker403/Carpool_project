

from collections import deque
from .models import Edge

def get_adjacency_list():
    
    adjacency = {}
    for edge in Edge.objects.select_related('source', 'destination').all():
        src = edge.source.id
        dst = edge.destination.id
        if src not in adjacency:
            adjacency[src] = []
        adjacency[src].append(dst)
    return adjacency

def bfs(start_node_id, end_node_id):
    
    graph = get_adjacency_list()
    visited = set()
    queue = deque([[start_node_id]])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end_node_id:
            return path

        if node in visited:
            continue
        visited.add(node)

        for neighbor in graph.get(node, []):
            queue.append(path + [neighbor])
