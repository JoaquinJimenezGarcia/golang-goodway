package conc

import "context"

// RunJobs runs jobs with bounded workers; returns results in completion order not required —
// tests sort. Each job is a func() int.
func RunJobs(ctx context.Context, workers int, jobs []func() int) ([]int, error) {
	// TODO
	return nil, nil
}
