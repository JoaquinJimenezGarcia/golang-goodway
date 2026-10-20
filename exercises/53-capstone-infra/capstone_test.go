package capstone

import "testing"

func TestJobQueue(t *testing.T) {
	var q JobQueue
	q.Enqueue("a")
	q.Enqueue("b")
	a, ok := q.Dequeue()
	if !ok || a != "a" {
		t.Fatal()
	}
}
