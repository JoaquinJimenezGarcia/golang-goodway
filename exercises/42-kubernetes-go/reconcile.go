package reconcile

type Object struct {
	Desired int
	Actual  int
}

// Reconcile mutates o.Actual toward Desired by at most 1 per call; returns whether done.
func Reconcile(o *Object) bool {
	// TODO
	return false
}
