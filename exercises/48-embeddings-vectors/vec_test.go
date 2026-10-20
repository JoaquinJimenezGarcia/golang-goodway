package vec

import "testing"

func TestCosine(t *testing.T) {
	a := []float64{1, 0}
	b := []float64{1, 0}
	if Cosine(a, b) < 0.999 {
		t.Fatal()
	}
}
