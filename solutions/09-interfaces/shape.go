package shape

type Shape interface {
	Area() float64
}

type Rect struct{ W, H float64 }

func (r Rect) Area() float64 { return r.W * r.H }

func TotalArea(shapes []Shape) float64 {
	var s float64
	for _, sh := range shapes {
		s += sh.Area()
	}
	return s
}
