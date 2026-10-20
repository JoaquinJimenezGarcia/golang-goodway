package algo

import "testing"

func TestBinarySearch(t *testing.T) {
	xs := []int{1, 3, 5, 7, 9}
	if BinarySearch(xs, 7) != 3 || BinarySearch(xs, 2) != -1 {
		t.Fatal()
	}
}
