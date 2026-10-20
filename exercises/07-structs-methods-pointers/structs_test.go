package structs

import "testing"

func TestCounter(t *testing.T) {
	c := NewCounter(2)
	c.Inc()
	if c.Value() != 3 {
		t.Fatalf("%d", c.Value())
	}
}
