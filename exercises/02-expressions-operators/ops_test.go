package ops

import "testing"

func TestSafeDiv(t *testing.T) {
	v, ok := SafeDiv(7, 2)
	if !ok || v != 3.5 {
		t.Fatalf("got %v %v", v, ok)
	}
	_, ok = SafeDiv(1, 0)
	if ok {
		t.Fatal("expected false")
	}
}

func TestClamp(t *testing.T) {
	if Clamp(5, 0, 10) != 5 || Clamp(-1, 0, 10) != 0 || Clamp(99, 0, 10) != 10 {
		t.Fatal("clamp failed")
	}
}
