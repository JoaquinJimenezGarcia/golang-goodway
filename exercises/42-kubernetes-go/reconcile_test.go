package reconcile

import "testing"

func TestReconcile(t *testing.T) {
	o := &Object{Desired: 3, Actual: 0}
	for i := 0; i < 10 && !Reconcile(o); i++ {
	}
	if o.Actual != 3 {
		t.Fatalf("%d", o.Actual)
	}
}
