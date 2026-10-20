package textx

func RuneCount(s string) int {
	n := 0
	for range s {
		n++
	}
	return n
}

func ReverseRunes(s string) string {
	r := []rune(s)
	for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	return string(r)
}
