package ctxx

import (
	"context"
	"testing"
	"time"
)

func TestSleepOrTimeout(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
	defer cancel()
	err := SleepOrTimeout(ctx, time.Second)
	if err == nil {
		t.Fatal("expected timeout error")
	}
}
