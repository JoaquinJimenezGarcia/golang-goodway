package capstone

type JobQueue struct {
	jobs []string
}

func (q *JobQueue) Enqueue(id string) { q.jobs = append(q.jobs, id) }

func (q *JobQueue) Dequeue() (string, bool) {
	if len(q.jobs) == 0 {
		return "", false
	}
	id := q.jobs[0]
	q.jobs = q.jobs[1:]
	return id, true
}
