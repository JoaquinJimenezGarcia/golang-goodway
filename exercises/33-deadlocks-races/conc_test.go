package conc

import (
	"context"
	"testing"
	"time"
)

func TestDrain(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	in := make(chan int)
	go func() {
		in <- 1
		in <- 2
		time.Sleep(20 * time.Millisecond)
		cancel()
	}()
	got := DrainUntilCancel(ctx, in)
	if len(got) < 1 {
		t.Fatalf("%v", got)
	}
}
