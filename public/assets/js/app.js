var stinfo = [];
var stwarn = [];
var sterr = [];


$(document).ready(function(){
    var socket = io.connect('http://lapitos.thebobsgamingnetwork.net:25576/log');
    
    socket.on('stout', function(msg)
    {        
        if(stinfo.length >=200)
        {
            stinfo.shift()
        }
        stinfo.push(msg.line)
        
        standard_log = '';
        for (var i = stinfo.length; i > 0; i--)
        {
            standard_log = standard_log + '<br/>' + stinfo[i -1];
        }
        $('#info').html(standard_log);
    })
    
    socket.on('stwarn', function(msg)
    {        
        if(stwarn.length >=200)
        {
            stwarn.shift()
        }
        stwarn.push(msg.line)
        
        warn_log = '';
        for (var i = stwarn.length; i > 0; i--)
        {
            warn_log = warn_log + '<br/>' + stwarn[i -1];
        }
        $('#warn').html(warn_log);
    })
    
    socket.on('sterr', function(msg)
    {
        if(sterr.length >=200)
        {
            sterr.shift()
        }
        sterr.push(msg.line)
        
        error_log = '';
        for (var i = sterr.length; i > 0; i--)
            {
                error_log = error_log + '<br/>' + sterr[i -1];
            }
        $('#error').html(error_log);
    })
});