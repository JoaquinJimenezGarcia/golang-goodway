package cache

import "testing"

func TestCacheAside(t *testing.T) {
	s := New(map[string]string{"a": "1"})
	v, ok := s.Get("a")
	if !ok || v != "1" {
		t.Fatal()
	}
	s.Set("a", "2")
	v, ok = s.Get("a")
	if !ok || v != "2" {
		t.Fatal()
	}
}
