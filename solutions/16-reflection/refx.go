package refx

import "reflect"

func KindName(v any) string {
	return reflect.TypeOf(v).Kind().String()
}
