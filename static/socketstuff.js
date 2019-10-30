
function socketStart(chart){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    socket.on('waveform', function(msg) {
        console.log("The deliciousness has landed");
        //console.log(JSON.stringify(msg.ch1));
        var ch1_vals = msg.ch1.ch1_points;
        var ch2_vals = msg.ch2.ch2_points;
        var time_vals = msg.ch1.time;
        var h_scale = msg.ch1.hscale;
        var v_scale = msg.ch1.vscale;
        var i = 0;
        var datum = [];
        for (i=0; i<ch1_vals.length; i++)
        {
            datum.push({'time':Number(time_vals[i]), 'value':Number(ch1_vals[i]), 'value2':Number(ch2_vals[i])});
        }
        //console.log(JSON.stringify(datum));
        chart.data = datum;
        // var time = Number(msg.number.time);
        // console.log("Time" + time.toString());
        // var sample = Number(msg.number.data);
        // console.log("Value" + sample.toString());
        // datum.addRow([time,sample]);
        // chart.draw(datum, options);
    });
    socket.on("connect", function(msg) {
        console.log("Connected papa");
    })
    $('form#form1').submit(function(event) {
        socket.emit('bussy', {data: 'poopy'});
        console.log("You're a poopyhead");
        return false;
    });
    $('form#form2').submit(function(event) {
        socket.emit('bussy', {data: 'head'});
        console.log("You're a poopyhead");
        return false;
    });

}