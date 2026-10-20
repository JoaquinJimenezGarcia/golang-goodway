package grpcex

func MethodPath(pkg, service, method string) string {
	return "/" + pkg + "." + service + "/" + method
}
