def process_a_json(filename):
    import json
    with open(filename, "r") as fp:
        chars = json.load(fp)
    return chars


if __name__ == "__main__":
    import sys
    for filename in sys.argv[1:]:
        parts = filename.split('/')[-1].split('.')[0].split('-')
        print(parts)
        freq_indices = list(map(int, parts))
        chars = process_a_json(filename)
        freqs = range(freq_indices[0], freq_indices[0] + len(chars))
        values = [{'char': char, "freq": freq} for (char, freq) in zip(chars, freqs)]
        import db
        from sqlalchemy.dialects.postgresql import insert
        stmt = insert(db.CHARACTERS_TABLE).values(values)
        on_update_stmt = stmt.on_conflict_do_update(
        index_elements=['char'],
        set_={"freq": stmt.excluded.freq}
        )
        ret = db.conn.execute(on_update_stmt)
        print(str(ret))

    db.conn.close()