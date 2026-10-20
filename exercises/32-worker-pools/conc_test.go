package conc

import (
	"context"
	"sort"
	"testing"
)

func TestRunJobs(t *testing.T) {
	jobs := []func() int{
		func() int { return 1 },
		func() int { return 2 },
		func() int { return 3 },
	}
	got, err := RunJobs(context.Background(), 2, jobs)
	if err != nil {
		t.Fatal(err)
	}
	sort.Ints(got)
	if len(got) != 3 || got[0] != 1 || got[2] != 3 {
		t.Fatalf("%v", got)
	}
}
