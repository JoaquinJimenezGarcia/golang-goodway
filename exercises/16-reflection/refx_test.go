package refx

import "testing"

func TestKindName(t *testing.T) {
	if KindName(3) != "int" || KindName("a") != "string" {
		t.Fatalf("%s %s", KindName(3), KindName("a"))
	}
}
