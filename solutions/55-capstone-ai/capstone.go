package capstone

import (
	"math"
	"sort"
)

type Doc struct {
	ID   string
	Text string
	Vec  []float64
}

func Cosine(a, b []float64) float64 {
	var dot, na, nb float64
	for i := range a {
		dot += a[i] * b[i]
		na += a[i] * a[i]
		nb += b[i] * b[i]
	}
	return dot / (math.Sqrt(na) * math.Sqrt(nb))
}

func TopK(docs []Doc, query []float64, k int) []Doc {
	type sc struct {
		d Doc
		s float64
	}
	scored := make([]sc, len(docs))
	for i, d := range docs {
		scored[i] = sc{d, Cosine(d.Vec, query)}
	}
	sort.Slice(scored, func(i, j int) bool { return scored[i].s > scored[j].s })
	if k > len(scored) {
		k = len(scored)
	}
	out := make([]Doc, k)
	for i := 0; i < k; i++ {
		out[i] = scored[i].d
	}
	return out
}
