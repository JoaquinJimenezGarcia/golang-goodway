package algo

import "testing"

func TestBloom(t *testing.T) {
	b := NewBloom(256, 3)
	b.Add("go")
	if !b.MightContain("go") {
		t.Fatal("should contain")
	}
}
