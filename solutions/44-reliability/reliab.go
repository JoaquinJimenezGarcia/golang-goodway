package reliab

import "sync"

type Runner struct {
	wg sync.WaitGroup
}

func (r *Runner) Start(fn func()) {
	r.wg.Add(1)
	go func() {
		defer r.wg.Done()
		fn()
	}()
}

func (r *Runner) Shutdown() { r.wg.Wait() }
