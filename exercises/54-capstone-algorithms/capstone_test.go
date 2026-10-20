package capstone

import (
	"reflect"
	"testing"
)

func TestIndex(t *testing.T) {
	idx := InvertedIndex{}
	idx.Add("d1", "Go is cool")
	idx.Add("d2", "go servers")
	got := idx.Query("go")
	want := []string{"d1", "d2"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("%v", got)
	}
}
