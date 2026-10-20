package httpsvc

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHealth(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rr := httptest.NewRecorder()
	HealthHandler(rr, req)
	if rr.Code != 200 || rr.Body.String() != "ok" {
		t.Fatalf("%d %q", rr.Code, rr.Body.String())
	}
}
