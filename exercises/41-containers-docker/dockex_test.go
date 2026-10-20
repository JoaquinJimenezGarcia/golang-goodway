package dockex

import (
	"strings"
	"testing"
)

func TestDockerfile(t *testing.T) {
	s := DockerfileMultiStage("example.com/app")
	for _, needle := range []string{"AS build", "CGO_ENABLED=0"} {
		if !strings.Contains(s, needle) {
			t.Fatalf("missing %s in %q", needle, s)
		}
	}
}
