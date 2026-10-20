package idiom

import (
	"fmt"
	"strings"
)

func ParsePairs(s string) (map[string]string, error) {
	out := map[string]string{}
	if s == "" {
		return out, nil
	}
	for _, part := range strings.Split(s, ",") {
		k, v, ok := strings.Cut(part, "=")
		if !ok || k == "" {
			return nil, fmt.Errorf("bad pair %q", part)
		}
		out[k] = v
	}
	return out, nil
}
