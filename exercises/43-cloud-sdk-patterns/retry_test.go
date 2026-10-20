package retry

import (
	"context"
	"errors"
	"testing"
)

func TestDo(t *testing.T) {
	n := 0
	err := Do(context.Background(), 3, func() error {
		n++
		if n < 3 {
			return errors.New("transient")
		}
		return nil
	})
	if err != nil || n != 3 {
		t.Fatalf("%v %d", err, n)
	}
}
