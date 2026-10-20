package algo

import "testing"

func TestTwoSum(t *testing.T) {
	i, j := TwoSum([]int{2, 7, 11, 15}, 9)
	if i == -1 || numsSum([]int{2, 7, 11, 15}, i, j) != 9 {
		t.Fatalf("%d %d", i, j)
	}
}

func numsSum(a []int, i, j int) int { return a[i] + a[j] }
