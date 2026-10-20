package infer

import "testing"

func TestQueue(t *testing.T) {
	q := NewQueue(1)
	if !q.Enqueue("a") || q.Enqueue("b") {
		t.Fatal("backpressure")
	}
	v, ok := q.Dequeue()
	if !ok || v != "a" {
		t.Fatal()
	}
}
