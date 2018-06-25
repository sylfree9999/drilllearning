---
title: sublimetext-usage
date: 2018-06-25 10:42:29
tags: [sublime, tips]
---

## Allow Alt+Drag in windows
I created a file "C:\Users\XX\AppData\Roaming\Sublime Text 3\Packages\User\Default (Windows).sublime-mousemap", and put this in it:

```
[
  {
    "button": "button1","modifiers": ["alt"],
    "press_command": "drag_select",
    "press_args": {"by": "columns"}
  },
]
```
restart Sublime