package rag

import "testing"

func TestChunk(t *testing.T) {
	got := Chunk("abcdefghij", 4, 2)
	if len(got) < 2 || got[0] != "abcd" {
		t.Fatalf("%v", got)
	}
}
