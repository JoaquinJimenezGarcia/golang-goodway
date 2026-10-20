package shape

import "testing"

func TestTotalArea(t *testing.T) {
	got := TotalArea([]Shape{Rect{2, 3}, Rect{1, 1}})
	if got != 7 {
		t.Fatalf("got %v", got)
	}
}
