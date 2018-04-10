drop table if exists courses;
create table courses (
    code text primary key not null,
    title text not null,
    prerequisite text,
    incompatible text,
    recommended_prerequisite text
);

create table programs (
    code text primary key not null,
    title text not null
);

create table majors (
    code text primary key not null,
    title text not null,
    pcode text references programs (code)
);


