package infer

type Queue struct {
	ch chan string
}

func NewQueue(depth int) *Queue {
	return &Queue{ch: make(chan string, depth)}
}

func (q *Queue) Enqueue(job string) bool {
	select {
	case q.ch <- job:
		return true
	default:
		return false
	}
}

func (q *Queue) Dequeue() (string, bool) {
	select {
	case v := <-q.ch:
		return v, true
	default:
		return "", false
	}
}
