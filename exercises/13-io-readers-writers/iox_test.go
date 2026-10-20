package iox

import (
	"strings"
	"testing"
)

func TestCountBytes(t *testing.T) {
	n, err := CountBytes(strings.NewReader("abcd"))
	if err != nil || n != 4 {
		t.Fatalf("%d %v", n, err)
	}
}
