var exec = require('child_process').exec; 

hexo.on('new', function(data){
   exec('start "" "C:\\Program Files\\Typora\\Typora.exe" ' + data.path);
  //exec('start "" "C:\\Program Files\\Sublime Text 3\\sublime_text.exe" ' + data.path);
});
