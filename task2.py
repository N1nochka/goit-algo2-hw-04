from collections import deque, defaultdict


class MaxFlow:
    def __init__(self):
        self.graph = defaultdict(lambda: defaultdict(int))
        self.capacity = defaultdict(lambda: defaultdict(int))

    def add_edge(self, u, v, c):
        self.graph[u][v] = c
        self.graph[v][u] = 0
        self.capacity[u][v] = c
        self.capacity[v][u] = 0

    def bfs(self, s, t, parent):
        visited = set([s])
        q = deque([s])

        while q:
            u = q.popleft()
            for v in self.graph[u]:
                if v not in visited and self.graph[u][v] > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == t:
                        return True
                    q.append(v)
        return False

    def edmonds_karp(self, s, t):
        max_flow = 0

        while True:
            parent = {}
            if not self.bfs(s, t, parent):
                break

            path_flow = float("inf")
            v = t

            while v != s:
                u = parent[v]
                path_flow = min(path_flow, self.graph[u][v])
                v = u

            v = t
            while v != s:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = u

            max_flow += path_flow

        return max_flow

    def get_flow(self, u, v):
        return self.capacity[u][v] - self.graph[u][v]


def build_graph():
    mf = MaxFlow()

    edges = [
        ("T1", "W1", 25), ("T1", "W2", 20), ("T1", "W3", 15),
        ("T2", "W3", 15), ("T2", "W4", 30), ("T2", "W2", 10),

        ("W1", "S1", 15), ("W1", "S2", 10), ("W1", "S3", 20),
        ("W2", "S4", 15), ("W2", "S5", 10), ("W2", "S6", 25),
        ("W3", "S7", 20), ("W3", "S8", 15), ("W3", "S9", 10),
        ("W4", "S10", 20), ("W4", "S11", 10), ("W4", "S12", 15),
        ("W4", "S13", 5), ("W4", "S14", 10),
    ]

    for u, v, c in edges:
        mf.add_edge(u, v, c)

    mf.add_edge("SOURCE", "T1", 60)
    mf.add_edge("SOURCE", "T2", 55)

    for i in range(1, 15):
        mf.add_edge(f"S{i}", "SINK", 100)

    return mf, edges


def main():
    mf, edges = build_graph()

    max_flow = mf.edmonds_karp("SOURCE", "SINK")

    print("=" * 60)
    print("MAX FLOW:", max_flow)
    print("=" * 60)

    print("\nТермінал → Магазин")
    print(f"{'Термінал':<10}{'Магазин':<10}{'Потік'}")

    terminals = ["T1", "T2"]

    for t in terminals:
        for i in range(1, 15):
            shop = f"S{i}"
            total = 0

            for u, v, _ in edges:
                if u == t:
                    total += mf.get_flow(u, v)

            print(f"{t:<10}{shop:<10}{total}")

    # ANALYSIS
    print("\n" + "=" * 60)
    print("АНАЛІЗ")
    print("=" * 60)

    # terminal comparison
    t1 = sum(mf.get_flow("T1", v) for v in ["W1", "W2", "W3"])
    t2 = sum(mf.get_flow("T2", v) for v in ["W2", "W3", "W4"])

    print(f"T1 total flow: {t1}")
    print(f"T2 total flow: {t2}")

    # bottlenecks
    print("\nВузькі місця:")
    for u, v, c in edges:
        used = mf.get_flow(u, v)
        if c <= 10:
            print(f"{u} → {v}: {used}/{c}")

    # warehouses load
    print("\nЗавантаження складів:")
    for w in ["W1", "W2", "W3", "W4"]:
        incoming = sum(mf.get_flow(t, w) for t in ["T1", "T2"] if w in mf.graph[t])
        outgoing = sum(mf.get_flow(w, f"S{i}") for i in range(1, 15) if f"S{i}" in mf.graph[w])

        print(f"{w}: in={incoming}, out={outgoing}")


if __name__ == "__main__":
    main()