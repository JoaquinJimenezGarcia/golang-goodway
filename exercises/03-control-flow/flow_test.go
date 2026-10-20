package flow

import (
	"reflect"
	"testing"
)

func TestFizzBuzz(t *testing.T) {
	got := FizzBuzz(5)
	want := []string{"1", "2", "Fizz", "4", "Buzz"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("got %v want %v", got, want)
	}
}

func TestClassify(t *testing.T) {
	if Classify(-1) != "neg" || Classify(0) != "zero" || Classify(2) != "pos" {
		t.Fatal("classify")
	}
}
