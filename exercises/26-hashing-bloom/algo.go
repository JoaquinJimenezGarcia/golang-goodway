package algo

type Bloom struct {
	bits []bool
	k    int
}

func NewBloom(size, k int) *Bloom {
	return &Bloom{bits: make([]bool, size), k: k}
}

func (b *Bloom) Add(s string) {
	// TODO set k bit positions derived from s
}

func (b *Bloom) MightContain(s string) bool {
	// TODO
	return false
}
