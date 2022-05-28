from sqlalchemy.dialects.postgresql import insert

def upsert(table, 
	rows, 
	# iw='id', 
	no_update_cols=['id']) -> None:

	stmt = insert(table).values(rows)

	update_cols = [c.name for c in table.c
									if c not in list(table.primary_key.columns)
									and c.name not in no_update_cols]

	on_conflict_stmt = stmt.on_conflict_do_update(
			index_elements=table.primary_key.columns,
			set_={k: getattr(stmt.excluded, k) for k in update_cols},
			# index_where=(getattr(table.c, iw) < getattr(stmt.excluded, iw))
			# where=(getattr(model.c, iw) < getattr(stmt.excluded, iw))
			)
	return on_conflict_stmt

# def upsert(table, rows):
# 	insert_stmt = insert(table).values(rows)
# 	on_duplicate_key_stmt = insert_stmt.on_conflict_do_update(
# 			set_={k: getattr(stmt.excluded, k) for k in update_cols},
# 		)
# 	return on_duplicate_key_stmt