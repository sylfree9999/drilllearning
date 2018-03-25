---
title: c# constructor chaining
date: 2018-03-25 16:19:49
tags: [c#, concept]
---

Consider this sample:

```
class Student {
	string _studengType = "";
	string _id = "";
	string _fName = "";
	string _lName = "";

	public Student(string id) : this(id, "", ""){

	}

	public Student(stirng id, string fName) : this(id, fName, ""){

	}

	public Student(string id, string fName, string lName){
		//Validation logic...
		_studentType = "<student_type>";

		_id = id;
		_fName = fName;
		_lName = lName;
	}
}
```

通过this，调用第三个构造参数，可以复用id赋值的这个语句：
`_id = id;`

这样就不用每个构造函数都写这个逻辑，只需要用那个有最多参数构造函数即可