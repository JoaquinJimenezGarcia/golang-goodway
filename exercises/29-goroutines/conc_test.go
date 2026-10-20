package conc

import "testing"

func TestParallelSum(t *testing.T) {
	xs := []int{1, 2, 3, 4, 5}
	if ParallelSum(xs, 2) != 15 {
		t.Fatal()
	}
}
