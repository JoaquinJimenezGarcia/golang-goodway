package infer

type Queue struct {
	ch chan string
}

func NewQueue(depth int) *Queue {
	return &Queue{ch: make(chan string, depth)}
}

// Enqueue returns false if queue full (backpressure).
func (q *Queue) Enqueue(job string) bool {
	// TODO non-blocking send
	return false
}

func (q *Queue) Dequeue() (string, bool) {
	// TODO
	return "", false
}
