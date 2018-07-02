---
title: net-linq
date: 2018-06-28 11:16:44
tags: [net, concept]
---

## linq to Object, 是翻译成object，在内存里面
```c#

//分页的功能
var list = studentList.Where(s=>s.Age<30)
			.Select(s => new
			{
				Id = s.Id,
				ClassId = s.ClassId,
				IdName = s.Id + s.Name,
				ClassName = s.ClassId == 2? "Advanced":"Other"
			})
			.OrderBy(s=>s.Id)
			.OrderByDescending(s=>s.ClassId)
			.Skip(2) //跳过几条
			.Take(3); //获取几条

//group
{
	var list = from s in studentList
				where s.Age < 30
				group s by s.ClassId into sg
				select new
				{
					key = sg.Key, //sg.Key就是s.ClassId
					maxAge = sg.Max(t=>t.Age)
				};

				//groupby new {s.ClassId,s.Age}
}

//inner join
{
	var list = from s in studentList
				join c in classList on s.ClassId equals c.Id
				select new
				{
					Name = s.Name,
					ClassName = c.ClassName
				};
}

//left join
{
	var list  = from s in studentList
				join c in classList on s.ClassId equals c.Id
				into scList
				from sc in scList.DefaultIfEmpty()
				select new
				{
					Name = s.Name,
					ClassName = sc==null?"无班级":sc.ClassName
				}
}

//left Join
{
	var list = studentList.Join(classList, s=>s.ClassId, c=>c.Id, (s,c)=>new{
			Name = s.Name,
			ClassName = c.ClassName
		}).DefaultIfEmpty();
}
```
