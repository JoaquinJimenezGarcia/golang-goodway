package mathx_test

import (
	"testing"

	"goodway/exercises/08-packages-modules/mathx"
)

func TestSquare(t *testing.T) {
	if mathx.Square(4) != 16 {
		t.Fatal()
	}
}
