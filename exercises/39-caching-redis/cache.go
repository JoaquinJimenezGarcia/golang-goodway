package cache

type Store struct {
	mem map[string]string
	db  map[string]string
}

func New(db map[string]string) *Store {
	return &Store{mem: map[string]string{}, db: db}
}

func (s *Store) Get(key string) (string, bool) {
	// TODO cache-aside
	return "", false
}

func (s *Store) Set(key, val string) {
	// TODO write db + invalidate/update cache
}
