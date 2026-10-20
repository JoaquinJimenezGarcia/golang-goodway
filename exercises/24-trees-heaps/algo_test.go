package algo

import "testing"

func TestMinHeap(t *testing.T) {
	var h MinIntHeap
	for _, v := range []int{5, 1, 3} {
		h.Push(v)
	}
	v, ok := h.Pop()
	if !ok || v != 1 {
		t.Fatalf("%v %v", v, ok)
	}
}
