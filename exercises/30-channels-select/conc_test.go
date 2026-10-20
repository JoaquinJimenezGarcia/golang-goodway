package conc

import (
	"reflect"
	"testing"
)

func TestSquares(t *testing.T) {
	in := make(chan int, 3)
	for _, v := range []int{1, 2, 3} {
		in <- v
	}
	close(in)
	var got []int
	for v := range Squares(in) {
		got = append(got, v)
	}
	if !reflect.DeepEqual(got, []int{1, 4, 9}) {
		t.Fatalf("%v", got)
	}
}
