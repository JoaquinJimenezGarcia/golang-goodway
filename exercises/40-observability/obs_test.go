package obs

import (
	"strings"
	"testing"
)

func TestFormatLog(t *testing.T) {
	s := FormatLog("info", "hi", map[string]string{"b": "2", "a": "1"})
	if !strings.Contains(s, "level=info") || !strings.Contains(s, "msg=hi") || !strings.Contains(s, "a=1") {
		t.Fatalf("%q", s)
	}
}
