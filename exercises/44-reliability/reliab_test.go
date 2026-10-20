package reliab

import (
	"sync/atomic"
	"testing"
	"time"
)

func TestShutdown(t *testing.T) {
	var r Runner
	var done atomic.Bool
	r.Start(func() {
		time.Sleep(30 * time.Millisecond)
		done.Store(true)
	})
	r.Shutdown()
	if !done.Load() {
		t.Fatal("shutdown returned early")
	}
}
