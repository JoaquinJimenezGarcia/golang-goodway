package capstone

type Doc struct {
	ID   string
	Text string
	Vec  []float64
}

func Cosine(a, b []float64) float64 {
	// TODO
	return 0
}

func TopK(docs []Doc, query []float64, k int) []Doc {
	// TODO return up to k docs by cosine desc
	return nil
}
