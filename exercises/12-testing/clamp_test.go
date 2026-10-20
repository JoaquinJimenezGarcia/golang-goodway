package clamp

import "testing"

func TestClamp(t *testing.T) {
	tests := []struct {
		name             string
		v, lo, hi, want  int
	}{
		{"mid", 5, 0, 10, 5},
		{"low", -1, 0, 10, 0},
		{"high", 99, 0, 10, 10},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := Clamp(tt.v, tt.lo, tt.hi); got != tt.want {
				t.Fatalf("got %d want %d", got, tt.want)
			}
		})
	}
}
