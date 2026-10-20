package capstone

// JobQueue is a tiny in-memory queue for the infra capstone starter.
type JobQueue struct {
	jobs []string
}

func (q *JobQueue) Enqueue(id string) {
	// TODO
}

func (q *JobQueue) Dequeue() (string, bool) {
	// TODO FIFO
	return "", false
}
