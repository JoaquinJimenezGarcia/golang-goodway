package retry

import "context"

func Do(ctx context.Context, attempts int, fn func() error) error {
	var err error
	for i := 0; i < attempts; i++ {
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
		}
		err = fn()
		if err == nil {
			return nil
		}
	}
	return err
}
