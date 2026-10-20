package agent

type ToolFunc func(args string) string

// RunLoop calls decide repeatedly. decide returns ("final", answer) or ("tool", name|args).
// Stop at maxSteps. tools maps name -> func.
func RunLoop(maxSteps int, decide func(history []string) (kind, payload string), tools map[string]ToolFunc) (string, error) {
	// TODO
	return "", nil
}
