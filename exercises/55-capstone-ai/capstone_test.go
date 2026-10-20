package capstone

import "testing"

func TestTopK(t *testing.T) {
	docs := []Doc{
		{ID: "a", Vec: []float64{1, 0}},
		{ID: "b", Vec: []float64{0.9, 0.1}},
		{ID: "c", Vec: []float64{0, 1}},
	}
	got := TopK(docs, []float64{1, 0}, 2)
	if len(got) != 2 || got[0].ID != "a" {
		t.Fatalf("%v", got)
	}
}
