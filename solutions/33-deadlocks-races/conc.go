package conc

import "context"

func DrainUntilCancel(ctx context.Context, in <-chan int) []int {
	var out []int
	for {
		select {
		case <-ctx.Done():
			return out
		case v, ok := <-in:
			if !ok {
				return out
			}
			out = append(out, v)
		}
	}
}
