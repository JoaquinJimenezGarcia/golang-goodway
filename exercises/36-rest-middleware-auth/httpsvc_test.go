package httpsvc

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestWithHeader(t *testing.T) {
	h := WithHeader(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(200)
	}), "X-Test", "1")
	rr := httptest.NewRecorder()
	h.ServeHTTP(rr, httptest.NewRequest("GET", "/", nil))
	if rr.Header().Get("X-Test") != "1" {
		t.Fatal()
	}
}
