package httpsvc

import "net/http"

func WithHeader(next http.Handler, key, val string) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set(key, val)
		next.ServeHTTP(w, r)
	})
}
