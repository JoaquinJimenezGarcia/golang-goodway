package algo

type Graph map[string][]string

func BFS(g Graph, start string) []string {
	seen := map[string]bool{start: true}
	q := []string{start}
	var order []string
	for len(q) > 0 {
		u := q[0]
		q = q[1:]
		order = append(order, u)
		for _, v := range g[u] {
			if !seen[v] {
				seen[v] = true
				q = append(q, v)
			}
		}
	}
	return order
}
