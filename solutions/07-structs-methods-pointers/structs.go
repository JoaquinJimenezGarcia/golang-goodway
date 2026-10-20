package structs

type Counter struct {
	n int
}

func NewCounter(start int) *Counter {
	return &Counter{n: start}
}

func (c *Counter) Inc() { c.n++ }

func (c *Counter) Value() int { return c.n }
