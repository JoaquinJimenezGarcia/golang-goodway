package fn

import "testing"

func TestParsePositive(t *testing.T) {
	v, err := ParsePositive("5")
	if err != nil || v != 5 {
		t.Fatalf("%v %v", v, err)
	}
	if _, err := ParsePositive("0"); err == nil {
		t.Fatal("want error for 0")
	}
	if _, err := ParsePositive("x"); err == nil {
		t.Fatal("want error for x")
	}
}
