package capstone

import "strings"

type InvertedIndex map[string][]string

func (idx InvertedIndex) Add(docID, text string) {
	for _, tok := range strings.Fields(strings.ToLower(text)) {
		list := idx[tok]
		found := false
		for _, d := range list {
			if d == docID {
				found = true
				break
			}
		}
		if !found {
			idx[tok] = append(list, docID)
		}
	}
}

func (idx InvertedIndex) Query(token string) []string {
	return idx[strings.ToLower(token)]
}
