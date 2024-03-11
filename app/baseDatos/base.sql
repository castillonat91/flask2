CREATE DATABASE AGENDA2024;
use AGENDA2024;

create table Personas(
idper int primary key auto_increment not null,
nombreper varchar(60) not null,
apellidoper varchar(60) not null,
emailper varchar(60) not null,
dirper varchar(60) not null,
telper varchar(60) not null,
usuarioper varchar(60) not null,
contraper varchar(60) not null
);
describe Personas;

use AGENDA2024;
select * from Personas;

