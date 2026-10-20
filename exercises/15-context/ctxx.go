package ctxx

import (
	"context"
	"time"
)

// SleepOrTimeout sleeps d unless ctx done first.
// Returns ctx.Err() if cancelled/timed out, else nil.
func SleepOrTimeout(ctx context.Context, d time.Duration) error {
	// TODO
	return nil
}
