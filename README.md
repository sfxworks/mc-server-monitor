# mc-server-monitor
I want a way to monitor the server without making a java plugin. This aims to solve that problem. 

Public facing files go in public. Host them wherever.

Run the watcher using python application.py path/to/logs ip.orhost.tobind.to P0RT

![Preview](https://raw.githubusercontent.com/sfxworks/mc-server-monitor/master/screenshots/preview.png)

Works like ssh.

TODO:
rcon & sockets for input
statistics and thinks based on log data
recounting of log data or even a /newlog path that always delivers from the begging of latest.log
