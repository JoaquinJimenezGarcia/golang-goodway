package errx

import (
	"errors"
	"fmt"
)

var ErrNotFound = errors.New("not found")

func WrapNotFound(id string) error {
	return fmt.Errorf("id %s: %w", id, ErrNotFound)
}

func IsNotFound(err error) bool {
	return errors.Is(err, ErrNotFound)
}
