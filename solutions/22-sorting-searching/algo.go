package algo

func BinarySearch(xs []int, target int) int {
	lo, hi := 0, len(xs)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if xs[mid] < target {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	if lo < len(xs) && xs[lo] == target {
		return lo
	}
	return -1
}
