---
title: SQL identity column increment suddenly jumps
date: 2018-03-15 16:29:45
tags: [sql,configuration,issue]
---

SQL SERVER 2016

{% asset_img sql_id_increment.jpg %}

SQL Server 2012 now uses a cache size of 1,000 when allocating IDENTITY values in an int column and restarting the service can "lose" unused values (The cache size is 10,000 for bigint/numeric).

Workarounds:

+ You can use a `SEQUENCE` instead of an identity column and define a smaller cache size for example and use `NEXT VALUE FOR` in a column default

e.g:

```sql
 CREATE SEQUENCE Service_Ticket_Seq AS INTEGER
 START WITH 1
 INCREMENT BY 1
 MINVALUE 1
 MAXVALUE 100
 CYCLE; 
```

We can put a `SEQUENCE` in the `DEFAULT` clause of the DDL for table:
```sql
CREATE TABLE Service_Tickets
(ticket_nbr INTEGER DEFAULT NEXT VALUE FOR Service_Ticket_Seq,
 department_code CHAR(1) NOT NULL
 CHECK (department_code IN ('M', 'F'))); 
```

Now play with code:
```sql
INSERT INTO Service_Tickets (department_code)
VALUES ('M');
 
SELECT * FROM Service_Tickets;
```

Now we get:

| ticket_nbr | department_code |
| :--------- | :-------------- |
| 1          | M               |


Let's re-do the Meats and Fish tables.
```
CREATE TABLE Meats
(ticket_seq INTEGER DEFAULT NEXT VALUE FOR Service_Ticket_Seq 
       PRIMARY KEY,
 meat_type VARCHAR(15) NOT NULL);
 
CREATE TABLE Fish
(ticket_seq INTEGER DEFAULT NEXT VALUE FOR Service_Ticket_Seq 
       PRIMARY KEY,
 fish_type VARCHAR(15) NOT NULL);
```

Now try:
```
INSERT INTO Meats (meat_type) VALUES ('pig');
INSERT INTO Fish (fish_type) VALUES ('squid');
SELECT * FROM Meats;
SELECT * FROM Fish;
```

We get:

| ticket_nbr | department_code |
| :--------- | :-------------- |
| 2          | pig             |
| 3          | squid           |

+ Apply trace flag 272 which makes the `IDENTITY` allocation logged as in previous versions.
	+ Run **SQL Server Configuration Manager**
	+ Select **SQL SERVER SERVICES**, right-click `SQL Server` and select `Properties`, select `Startup Parameters`, type `-T272` , Add, Apply, close and restart.

	 {% asset_img sql_server_config.jpg %}
