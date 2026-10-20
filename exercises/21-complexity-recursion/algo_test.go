package algo

import "testing"

func TestFib(t *testing.T) {
	want := []int{0, 1, 1, 2, 3, 5, 8}
	for i, w := range want {
		if Fib(i) != w {
			t.Fatalf("Fib(%d)=%d want %d", i, Fib(i), w)
		}
	}
}
