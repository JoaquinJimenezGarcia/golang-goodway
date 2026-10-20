package conc

import "sync"

type Counter struct {
	mu sync.Mutex
	n  int
}

func (c *Counter) Inc() {
	// TODO
}

func (c *Counter) Value() int {
	// TODO
	return 0
}
