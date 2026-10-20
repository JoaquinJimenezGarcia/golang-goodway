package algo

func TwoSum(nums []int, target int) (int, int) {
	seen := map[int]int{}
	for i, n := range nums {
		if j, ok := seen[target-n]; ok {
			return j, i
		}
		seen[n] = i
	}
	return -1, -1
}
