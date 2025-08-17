-- first init on the db 
-- we need a users table? what would we need? 
-- {'id': '104548192251719049823', 'email': 'acero.liangli@gmail.com', 'verified_email': True, 'name': 'Acero Liang Li', 'given_name': 'Acero', 'family_name': 'Liang Li', 'picture': 'https://lh3.googleusercontent.com/a/ACg8ocJljuWD9cWdODMfI51CeNSFzjoAZOPiWXztwl1Dbe9IKLkzmg=s96-c'}
-- we'll make use of Email, and 'given_name', that's it. Create users with that and that's it 
-- BIGSERIAL auto increments, so we can use it for a user id purpose 
-- google_sub is google's unique identifier for the user, everything else can change so we need it for the linkage purposes 
-- NOT NULL (just tells us it can't be null )
-- TIMESTAMPTZ: type that is a time stamp with the utc time zone, when queried, we get the time for the timezone im in which is perfect
-- DEFAULT sets the value automatically 
-- NOW() postgres function to return the time now 
-- to use this in the 
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    google_sub TEXT UNIQUE NOT NULL, 
    email TEXT UNIQUE NOT NULL,
    created_on TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ DEFAULT NOW()
);

-- psql commands
-- \list: shows all the dbs 
-- connect: 
-- \c <db_name>
-- \dt: shows all the tables
-- run the sql file 