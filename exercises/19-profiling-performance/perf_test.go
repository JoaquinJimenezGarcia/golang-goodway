package perf

import "testing"

func TestSumPrealloc(t *testing.T) {
	if SumPrealloc([]int{1, 2, 3}) != 6 {
		t.Fatal()
	}
}

func BenchmarkSumPrealloc(b *testing.B) {
	xs := make([]int, 10000)
	for i := 0; i < b.N; i++ {
		SumPrealloc(xs)
	}
}
