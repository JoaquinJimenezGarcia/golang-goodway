package genx

import (
	"reflect"
	"sort"
	"testing"
)

func TestMapKeys(t *testing.T) {
	ks := MapKeys(map[string]int{"b": 2, "a": 1})
	sort.Strings(ks)
	if !reflect.DeepEqual(ks, []string{"a", "b"}) {
		t.Fatalf("%v", ks)
	}
}

func TestFilter(t *testing.T) {
	got := Filter([]int{1, 2, 3, 4}, func(n int) bool { return n%2 == 0 })
	if !reflect.DeepEqual(got, []int{2, 4}) {
		t.Fatalf("%v", got)
	}
}
