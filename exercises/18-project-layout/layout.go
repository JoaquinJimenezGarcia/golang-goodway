package layout

// ClassifyPath returns "cmd", "internal", or "other" for a repo-relative path prefix.
func ClassifyPath(path string) string {
	// TODO: cmd/... => cmd; internal/... => internal; else other
	return ""
}
