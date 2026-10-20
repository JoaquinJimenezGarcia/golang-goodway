package grpcex

import "testing"

func TestMethodPath(t *testing.T) {
	if MethodPath("hw", "Greeter", "SayHello") != "/hw.Greeter/SayHello" {
		t.Fatal()
	}
}
