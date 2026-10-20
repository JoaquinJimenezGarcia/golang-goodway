package layout

import "strings"

func ClassifyPath(path string) string {
	switch {
	case strings.HasPrefix(path, "cmd/") || path == "cmd":
		return "cmd"
	case strings.HasPrefix(path, "internal/") || path == "internal":
		return "internal"
	default:
		return "other"
	}
}
