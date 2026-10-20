package algo

type MinIntHeap []int

func (h MinIntHeap) less(i, j int) bool { return h[i] < h[j] }

func (h *MinIntHeap) up(i int) {
	for i > 0 {
		p := (i - 1) / 2
		if !h.less(i, p) {
			break
		}
		(*h)[i], (*h)[p] = (*h)[p], (*h)[i]
		i = p
	}
}

func (h *MinIntHeap) down(i int) {
	n := len(*h)
	for {
		l := 2*i + 1
		if l >= n {
			break
		}
		j := l
		if r := l + 1; r < n && h.less(r, l) {
			j = r
		}
		if !h.less(j, i) {
			break
		}
		(*h)[i], (*h)[j] = (*h)[j], (*h)[i]
		i = j
	}
}

func (h *MinIntHeap) Push(v int) {
	*h = append(*h, v)
	h.up(len(*h) - 1)
}

func (h *MinIntHeap) Pop() (int, bool) {
	if len(*h) == 0 {
		return 0, false
	}
	v := (*h)[0]
	last := len(*h) - 1
	(*h)[0] = (*h)[last]
	*h = (*h)[:last]
	if len(*h) > 0 {
		h.down(0)
	}
	return v, true
}
