var exec = require('child_process').exec; 

hexo.on('new', function(data){
  _exec('start "" "C:\\Program Files\\Typora\\Typora.exe" ' + data.path);
});
