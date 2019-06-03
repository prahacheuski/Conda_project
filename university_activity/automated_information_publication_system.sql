drop schema if exists faculty cascade;
create schema faculty;

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

CREATE TABLE faculty.publication
(
    publication_id    serial,
    publication_name  character varying,
    publication_date  date,
    publication_place character varying,
    publication_type  faculty.publication_type,
    CONSTRAINT publication_publication_id_pkey PRIMARY KEY (publication_id)
);

CREATE TABLE faculty.publication_person_map
(
    person_id      integer,
    publication_id integer,
    CONSTRAINT publication_person_map_pkey PRIMARY KEY (person_id, publication_id),
    FOREIGN KEY (person_id) REFERENCES faculty.person (person_id),
    FOREIGN KEY (publication_id) REFERENCES faculty.publication (publication_id)
);

CREATE OR REPLACE FUNCTION faculty.verify_person_surname_is_valid()
    RETURNS trigger AS
$BODY$
begin
    IF new.person_surname ~ '^[A-Z]{1}[a-z]+$' THEN
        RETURN NEW;
    ELSE
        RAISE EXCEPTION 'Person surname "%" is not valid, it should start from one capital letter and have length at least 2 chars', new.person_surname;
    END IF;
end;
$BODY$
    LANGUAGE plpgsql VOLATILE
                     COST 100;

CREATE TRIGGER verify_person_valid_surname
    BEFORE INSERT OR UPDATE
    ON faculty.person
    FOR EACH ROW
EXECUTE PROCEDURE faculty.verify_person_surname_is_valid();

-- add persons
insert into faculty.person (person_surname, person_type)
values ('Ivanov', 'student'::faculty.person_type),
       ('Petrov', 'student'::faculty.person_type),
       ('Nesterov', 'PhD candidate'::faculty.person_type),
       ('Antonava', 'lecturer'::faculty.person_type),
       ('Zaya', 'other'::faculty.person_type);

-- show trigger works
insert into faculty.person (person_surname, person_type)
values ('ivanov', 'student'::faculty.person_type);

insert into faculty.person (person_surname, person_type)
values ('IVanov', 'student'::faculty.person_type);

insert into faculty.person (person_surname, person_type)
values ('I', 'student'::faculty.person_type);

insert into faculty.person (person_surname, person_type)
values ('Ivanov5', 'student'::faculty.person_type);

-- create SP for adding publications
CREATE OR REPLACE FUNCTION faculty.add_publication(publication_name varchar,
                                                   publication_date date,
                                                   publication_place varchar,
                                                   publication_type faculty.publication_type,
                                                   author_id_list integer[])
    RETURNS integer AS -- returns newly created publication id
$BODY$
DECLARE
    registered_ids integer[] := ARRAY(select person_id
                                      from faculty.person);
    id             integer;
    i_person_id    integer;
begin
    if cardinality(author_id_list) = 0 then
        RAISE EXCEPTION '"author_id_list" should contain at least one value';
    end if;

    if author_id_list @> registered_ids THEN
        RAISE EXCEPTION 'Not all values from "author_id_list" [%] exist in "faculty.person.person_id"',
            array_to_string(array(select unnest(author_id_list) except select unnest(registered_ids)), ', ', '*');
    end if;

    insert into faculty.publication (publication_name, publication_date, publication_place, publication_type)
    values (publication_name, publication_date, publication_place, publication_type) RETURNING publication_id into id;

    FOREACH i_person_id IN ARRAY author_id_list
        loop
            INSERT INTO faculty.publication_person_map VALUES (i_person_id, id);
            RAISE NOTICE 'Added mapping person_id=%/publication_id=%', i_person_id, id;
        end loop;

    return id;
end;
$BODY$
    LANGUAGE plpgsql VOLATILE
                     COST 100;

-- show function exeptions
select faculty.add_publication('Article: "Legacy education process"',
                               '03-06-2019',
                               'Minsk - BSU',
                               'article'::faculty.publication_type,
                               array []::int[]);

select faculty.add_publication('Article: "Legacy education process"',
                               '03-06-2019',
                               'Minsk - BSU',
                               'article'::faculty.publication_type,
                               array [1,2,3,4,5,6,7,8,9,10]::int[]);

-- add publications
select faculty.add_publication('Article: "Legacy education process"',
                               '31-05-2019',
                               'Minsk - BSU',
                               'article'::faculty.publication_type,
                               array [1,2,3]);

select faculty.add_publication('Book: "My Big Deal"',
                               '01-06-2019',
                               'Minsk',
                               'book'::faculty.publication_type,
                               array [3,4]);

select faculty.add_publication('Book: "My Big Deal"',
                               '02-06-2019',
                               'Brest',
                               'book'::faculty.publication_type,
                               array [3,4]);

select faculty.add_publication('Thesis: "Become successful person"',
                               '11-03-2015',
                               'Minsk National Library',
                               'thesis'::faculty.publication_type,
                               array [5]);

select faculty.add_publication('Book: "Become successful person"',
                               '01-06-2019',
                               'Minsk National Library',
                               'book'::faculty.publication_type,
                               array [5]);
