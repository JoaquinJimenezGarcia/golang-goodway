package iox

import "io"

func CountBytes(r io.Reader) (int, error) {
	buf := make([]byte, 512)
	total := 0
	for {
		n, err := r.Read(buf)
		total += n
		if err == io.EOF {
			return total, nil
		}
		if err != nil {
			return total, err
		}
	}
}
