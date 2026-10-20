package reliab

import "sync"

// Runner tracks in-flight work; Shutdown waits for all After Start completes.
type Runner struct {
	wg sync.WaitGroup
}

func (r *Runner) Start(fn func()) {
	// TODO
}

func (r *Runner) Shutdown() {
	// TODO
}
