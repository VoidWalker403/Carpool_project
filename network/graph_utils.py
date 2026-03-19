

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

from collections import deque
from .models import Edge, Node

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
    return None


def get_nodes_within_distance(node_ids, max_distance=2):
    """
    Given a list of node IDs (e.g. remaining route),
    return all node IDs reachable within max_distance hops.
    """
    graph = get_adjacency_list()
    # Also build reverse graph for incoming edges
    reverse_graph = {}
    for src, neighbors in graph.items():
        for dst in neighbors:
            if dst not in reverse_graph:
                reverse_graph[dst] = []
            reverse_graph[dst].append(src)

    reachable = set()
    for start in node_ids:
        # BFS forward
        visited = set()
        queue = deque([(start, 0)])
        while queue:
            node, dist = queue.popleft()
            if node in visited or dist > max_distance:
                continue
            visited.add(node)
            reachable.add(node)
            for neighbor in graph.get(node, []):
                queue.append((neighbor, dist + 1))
        # BFS backward
        visited = set()
        queue = deque([(start, 0)])
        while queue:
            node, dist = queue.popleft()
            if node in visited or dist > max_distance:
                continue
            visited.add(node)
            reachable.add(node)
            for neighbor in reverse_graph.get(node, []):
                queue.append((neighbor, dist + 1))

    return reachable


def calculate_detour(original_route, pickup_id, destination_id):
    """
    Calculate detour needed to serve a passenger.
    Returns (detour_node_ids, detour_distance) or (None, None) if impossible.
    original_route: list of node IDs (remaining route of driver)
    """
    graph = get_adjacency_list()

    # Find best insertion point for pickup and destination in the route
    best_cost = float('inf')
    best_detour = None

    for i in range(len(original_route)):
        # Try inserting pickup after position i
        before_pickup = original_route[i]
        path_to_pickup = bfs(before_pickup, pickup_id)
        if not path_to_pickup:
            continue

        for j in range(i, len(original_route)):
            # Try inserting destination after position j
            before_dest = pickup_id if j == i else original_route[j]
            path_to_dest = bfs(before_dest, destination_id)
            if not path_to_dest:
                continue

            # Reconnect to original route after destination
            if j + 1 < len(original_route):
                reconnect = bfs(destination_id, original_route[j + 1])
                if not reconnect:
                    continue
                extra = (len(path_to_pickup) - 2) + (len(path_to_dest) - 2) + (len(reconnect) - 2)
            else:
                extra = (len(path_to_pickup) - 2) + (len(path_to_dest) - 2)

            if extra < best_cost:
                best_cost = extra
                best_detour = path_to_pickup[1:] + path_to_dest[1:]

    if best_detour is None:
        return None, None

    return best_detour, best_cost


def calculate_fare(detour_distance, base_fare=5.00, per_node_rate=2.00):
    """Simple fare calculation based on detour distance."""
    return round(base_fare + (detour_distance * per_node_rate), 2)