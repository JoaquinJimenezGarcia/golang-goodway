package num

import "testing"

func TestDot(t *testing.T) {
	if Dot([]float64{1, 2}, []float64{3, 4}) != 11 {
		t.Fatal()
	}
	if !AlmostEqual(0.1+0.2, 0.3, 1e-9) {
		t.Fatal("eps")
	}
}
