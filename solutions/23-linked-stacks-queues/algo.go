package algo

type Stack []int

func (s *Stack) Push(v int) { *s = append(*s, v) }

func (s *Stack) Pop() (int, bool) {
	if len(*s) == 0 {
		return 0, false
	}
	i := len(*s) - 1
	v := (*s)[i]
	*s = (*s)[:i]
	return v, true
}
