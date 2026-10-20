package algo

import (
	"reflect"
	"testing"
)

func TestBFS(t *testing.T) {
	g := Graph{"A": {"B", "C"}, "B": {"D"}, "C": {}, "D": {}}
	got := BFS(g, "A")
	want := []string{"A", "B", "C", "D"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("%v", got)
	}
}
