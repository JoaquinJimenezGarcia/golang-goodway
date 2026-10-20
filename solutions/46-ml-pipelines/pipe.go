package pipe

func BatchChunks(xs []int, size int) [][]int {
	if size < 1 {
		return nil
	}
	var out [][]int
	for i := 0; i < len(xs); i += size {
		j := i + size
		if j > len(xs) {
			j = len(xs)
		}
		out = append(out, xs[i:j])
	}
	return out
}
