package jx

import (
	"encoding/json"
	"time"
)

type Event struct {
	ID string    `json:"id"`
	At time.Time `json:"at"`
}

func RoundTrip(e Event) (Event, error) {
	b, err := json.Marshal(e)
	if err != nil {
		return Event{}, err
	}
	var out Event
	if err := json.Unmarshal(b, &out); err != nil {
		return Event{}, err
	}
	return out, nil
}
