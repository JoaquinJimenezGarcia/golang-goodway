package conc

import "sync"

// ParallelSum sums xs using up to workers goroutines + WaitGroup.
func ParallelSum(xs []int, workers int) int {
	// TODO
	_ = sync.WaitGroup{}
	return 0
}
