package reconcile

type Object struct {
	Desired int
	Actual  int
}

func Reconcile(o *Object) bool {
	if o.Actual == o.Desired {
		return true
	}
	if o.Actual < o.Desired {
		o.Actual++
	} else {
		o.Actual--
	}
	return o.Actual == o.Desired
}
