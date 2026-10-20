package errx

import "testing"

func TestWrap(t *testing.T) {
	err := WrapNotFound("x")
	if !IsNotFound(err) {
		t.Fatal("expected NotFound")
	}
}
