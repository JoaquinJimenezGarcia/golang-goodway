package conc

import (
	"context"
	"sync"
)

func RunJobs(ctx context.Context, workers int, jobs []func() int) ([]int, error) {
	if workers < 1 {
		workers = 1
	}
	jobCh := make(chan func() int)
	resCh := make(chan int, len(jobs))
	var wg sync.WaitGroup
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := range jobCh {
				select {
				case <-ctx.Done():
					return
				default:
					resCh <- j()
				}
			}
		}()
	}
	for _, j := range jobs {
		jobCh <- j
	}
	close(jobCh)
	wg.Wait()
	close(resCh)
	out := make([]int, 0, len(jobs))
	for r := range resCh {
		out = append(out, r)
	}
	return out, ctx.Err()
}
