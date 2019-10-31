
function socketStart(chart_data){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    socket.on('waveform', function(msg) {
        console.log("The deliciousness has landed");
        //console.log(JSON.stringify(msg.ch1));
        var chart = chart_data.chart;
        var xAxis = chart_data.xAxis;
        var yAxis = chart_data.yAxis;
        var ch1_vals = msg.ch1.ch1_points;
        var ch2_vals = msg.ch2.ch2_points;
        var time_vals = msg.ch1.time;
        var h_scale = msg.ch1.hscale;
        var v_scale = msg.ch1.vscale;
        if (yAxis.max !== 4*v_scale) {
            yAxis.max = 4*v_scale;
            yAxis.min = -4*v_scale;
        }
        if (xAxis.max !== 4*h_scale) {
            xAxis.max = 4*h_scale;
            xAxis.min = -4*h_scale;
        }
        console.log(xAxis.max);
        console.log(xAxis.min);
        console.log(yAxis.max);
        console.log(yAxis.min);
        var i = 0;
        var datum = [];
/*        xAxis.max = 10;*/
        xAxis.min = xAxis.min - 1;
        //yAxis.min = yAxis.min - 1;
        xAxis.renderer.ticks.template.disabled = false;
        xAxis.renderer.ticks.template.strokeOpacity = 1;
        xAxis.renderer.ticks.template.stroke = am4core.color("#495C43");
        xAxis.renderer.ticks.template.strokeWidth = 2;
        xAxis.renderer.ticks.template.length = 10;
        yAxis.renderer.ticks.template.disabled = false;
        yAxis.renderer.ticks.template.strokeOpacity = 1;
        yAxis.renderer.ticks.template.stroke = am4core.color("#495C43");
        yAxis.renderer.ticks.template.strokeWidth = 2;
        yAxis.renderer.ticks.template.length = 10;
        for (i=0; i<ch1_vals.length; i++)
        {
            datum.push({'time':Number(time_vals[i]), 'value':Number(ch1_vals[i]), 'value2':Number(ch2_vals[i])});
        }
        //console.log(JSON.stringify(datum));
        chart.data = datum;
        xAxis.min = xAxis.min + 1;
        //yAxis.min = yAxis.min + 1;
        console.log(h_scale.toString() +"s/d " + v_scale.toString() + "V/d");
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

    $('form#scales').submit(function(event) {
        var h_scale = document.getElementById("hscale").valueOf();
        console.log(h_scale);
        var v_scale = document.getElementById("vscale").valueOf();
        console.log(v_scale);
        socket.emit('scales', {data: 'hageman', v_scale: v_scale, h_scale: h_scale});
        console.log("You're a poopyhead");
        return false;
    });

}