package collections

import (
	"reflect"
	"testing"
)

func TestSum(t *testing.T) {
	if Sum([]int{1, 2, 3}) != 6 {
		t.Fatal()
	}
}

func TestFreq(t *testing.T) {
	m := Freq([]string{"a", "b", "a"})
	if m["a"] != 2 || m["b"] != 1 {
		t.Fatalf("%v", m)
	}
}

func TestUnique(t *testing.T) {
	got := Unique([]int{1, 2, 1, 3, 2})
	want := []int{1, 2, 3}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("%v", got)
	}
}
