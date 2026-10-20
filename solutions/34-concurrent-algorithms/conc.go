package conc

import "sync"

func ParallelSum(xs []int, workers int) int {
	if workers < 1 {
		workers = 1
	}
	ch := make(chan int, len(xs))
	for _, v := range xs {
		ch <- v
	}
	close(ch)
	var wg sync.WaitGroup
	partial := make([]int, workers)
	for w := 0; w < workers; w++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			s := 0
			for v := range ch {
				s += v
			}
			partial[id] = s
		}(w)
	}
	wg.Wait()
	total := 0
	for _, p := range partial {
		total += p
	}
	return total
}
