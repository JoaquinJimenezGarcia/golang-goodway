package idiom

import "testing"

func TestParsePairs(t *testing.T) {
	m, err := ParsePairs("a=1,b=2")
	if err != nil || m["a"] != "1" || m["b"] != "2" {
		t.Fatalf("%v %v", m, err)
	}
	m, err = ParsePairs("")
	if err != nil || len(m) != 0 {
		t.Fatal("empty")
	}
}
