package evalx

type Case struct {
	Got, Want string
}

func ExactMatchAccuracy(cases []Case) float64 {
	if len(cases) == 0 {
		return 0
	}
	ok := 0
	for _, c := range cases {
		if c.Got == c.Want {
			ok++
		}
	}
	return float64(ok) / float64(len(cases))
}
