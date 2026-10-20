package evalx

import "testing"

func TestAcc(t *testing.T) {
	a := ExactMatchAccuracy([]Case{{"a", "a"}, {"b", "c"}})
	if a != 0.5 {
		t.Fatalf("%v", a)
	}
}
