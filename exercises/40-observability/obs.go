package obs

import "fmt"

// FormatLog returns key=value pairs joined by space for keys in stable order: level msg.
func FormatLog(level, msg string, kv map[string]string) string {
	// TODO include level and msg then sorted kv
	_ = fmt.Sprintf
	return ""
}
