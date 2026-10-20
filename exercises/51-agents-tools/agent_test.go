package agent

import "testing"

func TestRunLoop(t *testing.T) {
	steps := 0
	decide := func(h []string) (string, string) {
		steps++
		if steps == 1 {
			return "tool", "echo|hi"
		}
		return "final", "done:" + h[len(h)-1]
	}
	out, err := RunLoop(5, decide, map[string]ToolFunc{
		"echo": func(args string) string { return args },
	})
	if err != nil || out != "done:hi" {
		t.Fatalf("%q %v", out, err)
	}
}
