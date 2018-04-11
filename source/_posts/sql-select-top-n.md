---
title: SQL select top n 
date: 2018-04-11 17:53:07
tags: [MSSQL, practice]
---

If > SQL 2005,

```sql
select ExcelMediaPlanId,ChannelCN,rank
from(
	select ExcelMediaplanId, ChannelCN,Rank() 
	over (Partition BY ExcelMediaplanId order by UnitRatecard desc) as rank
	from ExcelAdPosition) rs 
where rank <=3
```

or 

```sql
WITH TOPTEN AS (
    SELECT *, ROW_NUMBER() 
    over (
        PARTITION BY [group_by_field] 
        order by [prioritise_field]
    ) AS RowNo 
    FROM [table_name]
)
SELECT * FROM TOPTEN WHERE RowNo <= 10
```

or 
```sql
select *
from Things t
where t.ThingID in (
    select top 10 ThingID
    from Things tt
    where tt.Section = t.Section and tt.ThingDate = @Date
    order by tt.DateEntered desc
    )
    and t.ThingDate = @Date
order by Section, DateEntered desc
```

In MS Access:

```sql
SELECT StudentID, TestID, TestScore
  FROM MyTable t
 WHERE TestID IN
(
  SELECT TOP 3 TestID 
    FROM MyTable
   WHERE StudentID = t.StudentID 
   ORDER BY TestScore DESC, TestID
)
 ORDER BY StudentID, TestScore DESC, TestID;
```

StudentID | TestID | Score
---- | ---
1 | 1 | 95
1 | 2 | 90
1	|	3	|	90
1	|	4	|	90
2	|	1	|	99
2	|	2	|	95
2	|	3	|	90
2	|	4	|	90