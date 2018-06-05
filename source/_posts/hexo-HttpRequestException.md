---
title: hexo-HttpRequestException
date: 2018-06-01 10:13:38
tags: [practice]
---

Hexo Error: HttpRequestException
```
warning: LF will be replaced by CRLF in tags/concept/index.html.
The file will have its original line endings in your working directory.
Fatal: HttpRequestException encountered.
bash: /dev/tty: No such device or address
error: failed to execute prompt script (exit code 1)
fatal: could not read Username for 'https://github.com': Invalid argument
FATAL Something's wrong. Maybe you can find the solution here: http://hexo.io/docs/troubleshooting.html
Error: Fatal: HttpRequestException encountered.
bash: /dev/tty: No such device or address
error: failed to execute prompt script (exit code 1)
fatal: could not read Username for 'https://github.com': Invalid argument

    at ChildProcess.<anonymous> (D:\learning\node_modules\hexo-util\lib\spawn.js:37:17)
    at emitTwo (events.js:126:13)
    at ChildProcess.emit (events.js:214:7)
    at ChildProcess.cp.emit (D:\learning\node_modules\cross-spawn\lib\enoent.js:40:29)
    at maybeClose (internal/child_process.js:925:16)
    at Process.ChildProcess._handle.onexit (internal/child_process.js:209:5)
```

使用：

```
git config --global credential.helper wincred

hexo clean
```