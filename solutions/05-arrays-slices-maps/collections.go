package collections

func Sum(xs []int) int {
	s := 0
	for _, v := range xs {
		s += v
	}
	return s
}

func Freq(words []string) map[string]int {
	m := make(map[string]int)
	for _, w := range words {
		m[w]++
	}
	return m
}

func Unique(xs []int) []int {
	seen := make(map[int]bool)
	out := make([]int, 0, len(xs))
	for _, v := range xs {
		if seen[v] {
			continue
		}
		seen[v] = true
		out = append(out, v)
	}
	return out
}
