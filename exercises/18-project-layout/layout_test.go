package layout

import "testing"

func TestClassifyPath(t *testing.T) {
	if ClassifyPath("cmd/api/main.go") != "cmd" {
		t.Fatal()
	}
	if ClassifyPath("internal/server/s.go") != "internal" {
		t.Fatal()
	}
	if ClassifyPath("pkg/x/x.go") != "other" {
		t.Fatal()
	}
}
