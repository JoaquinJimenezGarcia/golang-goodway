package jx

import "time"

type Event struct {
	ID string    `json:"id"`
	At time.Time `json:"at"`
}

func RoundTrip(e Event) (Event, error) {
	// TODO: marshal then unmarshal
	return Event{}, nil
}
