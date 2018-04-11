---
title: SSIS Cannot Import Package
date: 2018-03-26 15:51:46
tags: [SSIS, issue]
---

Error:

```
The SQL Server instance specified in SSIS service configuration is not present or is not available. This might occur when there is no default instance of SQL Server on the computer. For more information, see the topic "Configuring the Integration Services Service" in Server 2008 Books Online.

Login failed for user 'XXXXX'. (MsDtsSrvr)
```

Solution:

Add the user XXXX as a login to the SQL server 
with sys_admin rights to msdb