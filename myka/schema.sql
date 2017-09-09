drop table if exists titles;
create table titles (
  id integer primary key,
  lang char(2) not null,
  'text' text not null
);


-- .open myka.db
-- .separator "\t"
-- .import ./data/myka.tsv titles
