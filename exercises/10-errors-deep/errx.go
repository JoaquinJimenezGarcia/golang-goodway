package errx

import "fmt"

var ErrNotFound = fmt.Errorf("not found")

func WrapNotFound(id string) error {
	// TODO: wrap ErrNotFound with id using %w
	return nil
}

func IsNotFound(err error) bool {
	// TODO: errors.Is
	return false
}
