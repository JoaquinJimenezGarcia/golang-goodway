package basics

import "fmt"

func ZeroInt() int {
	var n int
	return n
}

func Describe(n int, label string) string {
	return fmt.Sprintf("%s=%d", label, n)
}
