package cache

type Store struct {
	mem map[string]string
	db  map[string]string
}

func New(db map[string]string) *Store {
	return &Store{mem: map[string]string{}, db: db}
}

func (s *Store) Get(key string) (string, bool) {
	if v, ok := s.mem[key]; ok {
		return v, true
	}
	v, ok := s.db[key]
	if !ok {
		return "", false
	}
	s.mem[key] = v
	return v, true
}

func (s *Store) Set(key, val string) {
	s.db[key] = val
	delete(s.mem, key)
}
