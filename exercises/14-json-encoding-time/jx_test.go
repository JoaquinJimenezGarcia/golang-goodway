package jx

import (
	"testing"
	"time"
)

func TestRoundTrip(t *testing.T) {
	in := Event{ID: "1", At: time.Date(2024, 1, 2, 3, 4, 5, 0, time.UTC)}
	out, err := RoundTrip(in)
	if err != nil {
		t.Fatal(err)
	}
	if out.ID != in.ID || !out.At.Equal(in.At) {
		t.Fatalf("%+v", out)
	}
}
