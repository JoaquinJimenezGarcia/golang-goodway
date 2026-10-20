package ops

func SafeDiv(a, b int) (float64, bool) {
	if b == 0 {
		return 0, false
	}
	return float64(a) / float64(b), true
}

func Clamp(v, lo, hi int) int {
	if v < lo {
		return lo
	}
	if v > hi {
		return hi
	}
	return v
}
