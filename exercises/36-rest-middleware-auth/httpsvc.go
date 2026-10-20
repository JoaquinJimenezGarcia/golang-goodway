package httpsvc

import "net/http"

func WithHeader(next http.Handler, key, val string) http.Handler {
	// TODO set response header then call next
	return next
}
