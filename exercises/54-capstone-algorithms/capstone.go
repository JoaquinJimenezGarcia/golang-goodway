package capstone

// InvertedIndex maps token -> doc IDs.
type InvertedIndex map[string][]string

func (idx InvertedIndex) Add(docID, text string) {
	// TODO lowercase split on spaces; append docID if not present
}

func (idx InvertedIndex) Query(token string) []string {
	// TODO
	return nil
}
