package fn

import (
	"fmt"
	"strconv"
)

func ParsePositive(s string) (int, error) {
	n, err := strconv.Atoi(s)
	if err != nil {
		return 0, err
	}
	if n <= 0 {
		return 0, fmt.Errorf("need positive, got %d", n)
	}
	return n, nil
}
