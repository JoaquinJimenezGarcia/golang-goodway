package pipe

import (
	"reflect"
	"testing"
)

func TestBatch(t *testing.T) {
	got := BatchChunks([]int{1, 2, 3, 4, 5}, 2)
	want := [][]int{{1, 2}, {3, 4}, {5}}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("%v", got)
	}
}
