

@app.get("/api/registrations")
def list_registrations():
    rows = run_sql(
        "SELECT id, name, event, created FROM registrations ORDER BY id",
        fetch=True,
    )
    return jsonify([
        {
            "id": i,
            "name": n,
            "event": e,
            "created": c.isoformat(timespec="seconds"),
        }
        for i, n, e, c in rows
    ])


@app.post("/api/registrations")
def add_registration():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    event = str(data.get("event", "")).strip()

    if not name or not event:
        return jsonify(error="name and event are required"), 400

    new_id = run_sql(
        "INSERT INTO registrations (name, event) VALUES (%s, %s) RETURNING id",
        (name, event),
        fetch=True,
    )[0][0]

    return jsonify(id=new_id, name=name, event=event), 201


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    app.run(host="0.0.0.0", port=5000)
