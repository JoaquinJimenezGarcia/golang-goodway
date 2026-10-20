package sqlx

import (
	"strings"
	"testing"
)

func TestUserByIDQuery(t *testing.T) {
	q, args := UserByIDQuery("abc")
	if strings.Contains(q, "abc") {
		t.Fatal("id embedded in query")
	}
	if len(args) != 1 || args[0] != "abc" {
		t.Fatalf("%v", args)
	}
}
