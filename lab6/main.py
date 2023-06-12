from multiprocessing import Pool, current_process, Array, Process

graph = {
    0: [1, 3],
    1: [2, 4],
    2: [5],
    3: [4, 6],
    4: [5, 7],
    5: [8],
    6: [7],
    7: [8],
    8: []
}

# 0 1 2
# 3 4 5
# 6 7 8


def doIT():
    # e, tree = arr[0], arr[1]
    # print(tree)
    # e1 = []
    # for edge in e:
    #     if tree[edge[0]] == -1:
    #         e1.append(edge)
    e1 = Array("i", range(2))
    e1[0]=4
    e1[1]=2
    return e1

def bfs(s, G):
    front = [s]
    tree = [-1 for _ in range(len(G.keys()))]
    tree[s] = s
    while len(front) != 0:
        e = []
        for v in front:
            for u in G[v]:
                e.append([u, v])
            # e.append(1)
            # E.append(u, v): u ∈ G[v]) // reprezentacja – lista list

        e1 = []
        for edge in e:
            if tree[edge[0]] == -1:
                e1.append(edge)

        # e1 = doIT()
        # p = Pool(2)
        #
        # ar = p.map(doIT, [])
        # p.close()
        # p.join()
        # print()
        # print(ar)
        # print(e1)

        # for edge in e1:
        #     tree[edge[0]] = edge[1]

        def fun(tree, pair):
            u, v = pair
            tree[u] = v

        P = [Process(target=fun, args = (tree, pair) )for pair in e1]
        for p in P:
            p.start()
        for p in P:
            p.join()

        front = []
        for edge in e1:
            if tree[edge[0]] == edge[1]:
                front.append(edge[0])
    return tree
    #     e1 = [[1, 2]]
    #     tree = tree
    # print(tree)
    # # tree[]
    # visited = [s]
    # queue = [s]
    #
    # while queue:
    #     m = queue.pop(0)
    #     print(m, end=" ")
    #
    #     for neighbour in G[m]:
    #         if neighbour not in visited:
    #             visited.append(neighbour)
    #             queue.append(neighbour)


print(bfs(0, graph))
