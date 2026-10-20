package agent

import (
	"fmt"
	"strings"
)

type ToolFunc func(args string) string

func RunLoop(maxSteps int, decide func(history []string) (kind, payload string), tools map[string]ToolFunc) (string, error) {
	var history []string
	for step := 0; step < maxSteps; step++ {
		kind, payload := decide(history)
		switch kind {
		case "final":
			return payload, nil
		case "tool":
			name, args, _ := strings.Cut(payload, "|")
			fn, ok := tools[name]
			if !ok {
				return "", fmt.Errorf("unknown tool %s", name)
			}
			history = append(history, fn(args))
		default:
			return "", fmt.Errorf("unknown kind %s", kind)
		}
	}
	return "", fmt.Errorf("max steps")
}
