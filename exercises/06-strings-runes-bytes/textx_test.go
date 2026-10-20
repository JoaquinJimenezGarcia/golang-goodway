package textx

import "testing"

func TestRuneCount(t *testing.T) {
	if RuneCount("Go👍") != 3 {
		t.Fatalf("got %d", RuneCount("Go👍"))
	}
}

func TestReverseRunes(t *testing.T) {
	if ReverseRunes("ab👍") != "👍ba" {
		t.Fatalf("got %q", ReverseRunes("ab👍"))
	}
}
