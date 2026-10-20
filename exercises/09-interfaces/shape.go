package shape

type Shape interface {
	Area() float64
}

type Rect struct{ W, H float64 }

func (r Rect) Area() float64 {
	// TODO
	return 0
}

// TotalArea sums areas.
func TotalArea(shapes []Shape) float64 {
	// TODO
	return 0
}
