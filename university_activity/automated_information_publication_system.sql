-- Create specific data types
CREATE TYPE faculty.person_type AS ENUM ('student', 'PhD candidate', 'lecturer', 'other');
CREATE TYPE faculty.publication_type AS ENUM ('book', 'article', 'report', 'thesis', 'other');

-- Create general tables, functions, triggers
CREATE TABLE faculty.person
(
    person_id      serial,
    person_surname character varying,
    person_type    faculty.person_type,
    CONSTRAINT person_person_id_pkey PRIMARY KEY (person_id)
);

CREATE OR REPLACE FUNCTION faculty.at_leat_one(in_arr integer[])
    RETURNS boolean AS
$BODY$
begin
    IF array_length(in_arr, 1) >= 1 THEN
        return true;
    ELSE
        return false;
    END IF;
end;
$BODY$
    LANGUAGE plpgsql VOLATILE
                     COST 100;

CREATE TABLE faculty.group
(
    group_name character varying,
    persons    integer[] not null,
    CONSTRAINT group_group_name_pkey PRIMARY KEY (group_name),
    CONSTRAINT at_leat_one_person CHECK (faculty.at_leat_one(persons))
);

CREATE OR REPLACE FUNCTION faculty.verify_all_persons_are_exist()
    RETURNS trigger AS
$BODY$
DECLARE
    registered_ids integer[] := ARRAY(select person_id
                                      from faculty.person);
begin
    IF new.persons <@ registered_ids THEN
        RETURN NEW;
    ELSE
        RAISE EXCEPTION 'Not all values from "faculty.group.persons" [%] exist in "faculty.person.person_id"',
            array_to_string(array(select unnest(new.persons) except select unnest(registered_ids)), ', ', '*');
    END IF;
end;
$BODY$
    LANGUAGE plpgsql VOLATILE
                     COST 100;

CREATE TRIGGER verify_person_integrity
    BEFORE INSERT OR UPDATE
    ON faculty.group
    FOR EACH ROW
EXECUTE PROCEDURE faculty.verify_all_persons_are_exist();

CREATE TABLE faculty.publication
(
    publication_id    serial,
    group_name        character varying not null,
    publication_name  character varying,
    publication_date  date,
    publication_place character varying,
    publication_type  faculty.publication_type,
    CONSTRAINT publication_publication_id_pkey PRIMARY KEY (publication_id),
    FOREIGN KEY (group_name) REFERENCES faculty.group (group_name)
);

-- add persons
insert into faculty.person (person_surname, person_type)
values ('Ivanov', 'student'::faculty.person_type),
       ('Petrov', 'student'::faculty.person_type),
       ('Nesterov', 'PhD candidate'::faculty.person_type),
       ('Antonava', 'lecturer'::faculty.person_type),
       ('Zaya', 'other'::faculty.person_type);

-- divide persons into 3 groups
insert into faculty.group (group_name, persons)
values ('friendly guys', array [1, 2]),
       ('clever couple', array [4, 5]),
       ('single person Nesterov', array [3]);

-- show trigger works
insert into faculty.group (group_name, persons)
values ('invalid data', array [-1]);

-- show check constraint works
insert into faculty.group (group_name, persons)
values ('invalid data', array []::integer[]);

-- add publications
insert into faculty.publication (group_name, publication_name, publication_date, publication_place, publication_type)
values ('friendly guys', 'Article: "Legacy education process"', '31-05-2019', 'Minsk - BSU',
        'article'::faculty.publication_type),
       ('clever couple', 'Book: "My Big Deal"', '01-06-2019', 'Minsk', 'book'::faculty.publication_type),
       ('clever couple', 'Book: "My Big Deal"', '02-06-2019', 'Brest', 'book'::faculty.publication_type),
       ('single person Nesterov', 'Thesis: "Become successful person"', '11-03-2015', 'Minsk National Library',
        'thesis'::faculty.publication_type),
       ('single person Nesterov', 'Book: "Become successful person"', '01-06-2019', 'Minsk National Library',
        'book'::faculty.publication_type);
