package sqlx

func UserByIDQuery(id string) (query string, args []any) {
	return `SELECT name FROM users WHERE id=$1`, []any{id}
}
