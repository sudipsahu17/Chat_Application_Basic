var socket;
$(document).ready(function(){

    var textarea = document.getElementById('chat');
    textarea.scrollTop = textarea.scrollHeight;

    var uri = location.protocol + '//' + document.domain + ':' + location.port;
    socket = io.connect(uri);

    socket.on('connect', function() {
		//socket.send(username  + ' is online !!');
		socket.emit('join', {"username" : username, "room": room});
	});

	socket.on('message', function(data) {
	    var msg = data.msg;
	    var username = data.username;
	    var time_stamp = data.time_stamp;
		$("#chat").append(username + " (" + time_stamp + ") : " + msg + '\n');
		textarea.scrollTop = textarea.scrollHeight;
	});

	$('#send').on('click', function() {
		var msg = $('#text').val().trim();
		if (msg) {
		    socket.emit('user_message', {"msg": msg, 'username': username, "room": room, "uid": uid});
		}
		$('#text').val('');
	});

});

function leave_room() {
    socket.emit('leave', {"username" : username, "room": room}, function() {
        socket.disconnect();
        window.location.href = '/groups';
    });
}