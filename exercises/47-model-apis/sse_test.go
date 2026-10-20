package sse

import (
	"reflect"
	"testing"
)

func TestParse(t *testing.T) {
	s := "data: hi\n\ndata: there\n\ndata: [DONE]\n\n"
	got := ParseDataLines(s)
	want := []string{"hi", "there"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("%v", got)
	}
}
