CREATE TABLE if not exists users (
    id BIGSERIAL PRIMARY KEY,
    google_sub TEXT UNIQUE NOT NULL, 
    email TEXT UNIQUE NOT NULL,
    created_on TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE if not exists agent_state (
    agent_id BIGSERIAL PRIMARY KEY,
    agent_messages JSONB NOT NULL,
    sheet_status text[][] NOT NULL
);

CREATE TABLE if not exists sheets(
    id BIGSERIAL PRIMARY KEY,
    sheet_name TEXT not NULL,
    sheet_status text[][] NOT NULL,
    last_update_time TIMESTAMPTZ NOT NULL,
    user_id BIGINT references users(id)
);

CREATE INDEX ON sheets (user_id);