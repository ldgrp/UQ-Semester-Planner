drop table if exists courses;
create table courses (
    id integer primary key autoincrement,
    title text not null,
    'code' text not null
);
