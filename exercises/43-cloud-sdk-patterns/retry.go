package retry

import "context"

// Do retries fn on error until success or ctx done. attempts counts tries.
func Do(ctx context.Context, attempts int, fn func() error) error {
	// TODO
	return nil
}
