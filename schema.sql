DROP TABLE tasks;

CREATE TABLE projects (
	id serial primary key,
	user_id int default 1,
	created timestamp default 'now',
	name text,
	parent_id int references projects,
	last_reviewed date
);

CREATE TABLE tasks (
	id serial primary key,
	user_id int default 1,
	created timestamp default 'now',
	completed timestamp,
	postponed_until date,
	someday boolean,
	name text,
	project_id int references projects,
	stalled boolean default 'f',
	gave_up boolean
);

insert into projects (name) values ('rtask');
insert into tasks (name) values ('Get initial version working');