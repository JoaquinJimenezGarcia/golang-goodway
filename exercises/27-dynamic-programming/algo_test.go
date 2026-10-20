package algo

import "testing"

func TestClimb(t *testing.T) {
	if ClimbStairs(1) != 1 || ClimbStairs(2) != 2 || ClimbStairs(3) != 3 || ClimbStairs(4) != 5 {
		t.Fatal()
	}
}
