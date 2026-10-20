package algo

import "testing"

func TestStack(t *testing.T) {
	var s Stack
	s.Push(1)
	s.Push(2)
	v, ok := s.Pop()
	if !ok || v != 2 {
		t.Fatal()
	}
}
