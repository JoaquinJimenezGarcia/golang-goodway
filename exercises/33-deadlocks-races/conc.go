package conc

import "context"

// DrainUntilCancel reads from in until ctx done or in closed; returns values read.
func DrainUntilCancel(ctx context.Context, in <-chan int) []int {
	// TODO
	return nil
}
