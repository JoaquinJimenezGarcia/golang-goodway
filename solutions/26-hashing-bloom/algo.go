package algo

type Bloom struct {
	bits []bool
	k    int
}

func NewBloom(size, k int) *Bloom {
	return &Bloom{bits: make([]bool, size), k: k}
}

func (b *Bloom) hashes(s string) []int {
	out := make([]int, b.k)
	var h uint64 = 14695981039346656037
	for i := 0; i < b.k; i++ {
		for _, c := range s {
			h ^= uint64(c) + uint64(i)
			h *= 1099511628211
		}
		out[i] = int(h % uint64(len(b.bits)))
	}
	return out
}

func (b *Bloom) Add(s string) {
	for _, i := range b.hashes(s) {
		b.bits[i] = true
	}
}

func (b *Bloom) MightContain(s string) bool {
	for _, i := range b.hashes(s) {
		if !b.bits[i] {
			return false
		}
	}
	return true
}
