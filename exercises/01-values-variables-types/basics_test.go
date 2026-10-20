package basics

import "testing"

func TestZeroInt(t *testing.T) {
	if ZeroInt() != 0 {
		t.Fatalf("want 0")
	}
}

func TestDescribe(t *testing.T) {
	if Describe(3, "count") != "count=3" {
		t.Fatalf("got %q", Describe(3, "count"))
	}
}
