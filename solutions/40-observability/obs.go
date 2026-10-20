package obs

import (
	"fmt"
	"sort"
	"strings"
)

func FormatLog(level, msg string, kv map[string]string) string {
	parts := []string{fmt.Sprintf("level=%s", level), fmt.Sprintf("msg=%s", msg)}
	keys := make([]string, 0, len(kv))
	for k := range kv {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	for _, k := range keys {
		parts = append(parts, fmt.Sprintf("%s=%s", k, kv[k]))
	}
	return strings.Join(parts, " ")
}
