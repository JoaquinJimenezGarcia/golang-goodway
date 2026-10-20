package fn

import "strconv"

// ParsePositive parses s as int; returns error if not an int or if <= 0.
func ParsePositive(s string) (int, error) {
	// TODO: use strconv.Atoi
	_ = strconv.Atoi
	return 0, nil
}
