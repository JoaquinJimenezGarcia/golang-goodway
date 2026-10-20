package dockex

// DockerfileMultiStage returns a minimal multi-stage Dockerfile string for module path app.
func DockerfileMultiStage(modulePath string) string {
	// TODO must contain "AS build" and "CGO_ENABLED=0" and "nonroot" or "scratch"/"distroless"
	return ""
}
