package rag

func Chunk(s string, size, overlap int) []string {
	r := []rune(s)
	if size < 1 {
		return nil
	}
	if overlap >= size {
		overlap = size - 1
	}
	var out []string
	for start := 0; start < len(r); {
		end := start + size
		if end > len(r) {
			end = len(r)
		}
		out = append(out, string(r[start:end]))
		if end == len(r) {
			break
		}
		start = end - overlap
	}
	return out
}
