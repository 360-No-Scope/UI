
function socketStart(chart_data){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var measList = [];
    socket.on('waveform', function(msg) {
        console.log("The deliciousness has landed");
        //console.log(JSON.stringify(msg.ch1));
        var chart = chart_data.chart;
        var xAxis = chart_data.xAxis;
        var yAxis = chart_data.yAxis;
        var ch1_vals = msg.ch1.ch1_points;
        //var ch2_vals = msg.ch2.ch2_points;
        var time_vals = msg.ch1.time;
        var h_scale = msg.ch1.hscale;
        var v_scale = msg.ch1.vscale;
        console.log(h_scale + " horizontal");
        console.log(v_scale + " verticle");
        //console.log(msg.ch3.toString());
        if (yAxis.max !== v_scale/2.0) {
            yAxis.max = v_scale/2.0;
            yAxis.min = -v_scale/2.0;
        }
        if (xAxis.max !== Math.abs(h_scale/2)) {
            console.log("Adjusting dadeee");
            xAxis.max = Math.abs(h_scale/2.0);
            console.log(Math.abs(h_scale/2.0));
            xAxis.min = -Math.abs(h_scale/2.0);
        }
        if (xAxis.max !== -xAxis.min) {
            console.log("Wu oh it's uneven Kimmy pie");
            xAxis.min = -xAxis.max
        }
        console.log(xAxis.max);
        console.log(xAxis.min);
        //console.log(yAxis.max);
        //console.log(yAxis.min);
        var frequency = msg.ch1.meas[0];
        if (frequency === 69420) {
            frequency = Infinity;
        }
        var pkpk = msg.ch1.meas[1];
        var period = msg.ch1.meas[2];
        if (period === 69420) {
            period = Infinity;
        }
        var delta_time = msg.ch1.meas[3];
        var delta_volt = msg.ch1.meas[4];
        var duty = msg.ch1.meas[5];
        var neg_duty = msg.ch1.meas[6];
        var rising_cnt = msg.ch1.meas[7];
        var falling_cnt = msg.ch1.meas[8];
        // Checking and updating measurements list
        for(var i =0; i<measList.length;i++)
        {
            if (measList[i] === "Frequency") {
                document.getElementById("Frequency").innerHTML = ("Frequency: " + frequency.toString() + "Hz");
            }
            else if (measList[i] === "Pk-Pk_Voltage") {
                document.getElementById("Pk-Pk_Voltage").innerHTML = ("Pk-Pk Voltage: " + pkpk.toString() + "V");
            }
            else if (measList[i] === "Period") {
                document.getElementById("Period").innerHTML = ("Period: " + period.toString() + " s");
            }
            else if (measList[i] === "Delta_Time") {
                document.getElementById("Delta_Time").innerHTML = ("Delta Time: " + delta_time.toString() + "s");
            }
            else if (measList[i] === "Delta_Voltage") {
                document.getElementById("Delta_Voltage").innerHTML = ("Delta Voltage: " + delta_volt.toString() + "V");
            }
            else if (measList[i] === "Duty_Cycle") {
                document.getElementById("Duty_Cycle").innerHTML = ("Duty Cycle: " + duty.toString());
            }
            else if (measList[i] === "Rising_Count") {
                document.getElementById("Rising_Count").innerHTML = ("Rising Count: " + rising_cnt.toString());
            }
            else if (measList[i] === "Neg_Duty_Cycle") {
                document.getElementById("Neg_Duty_Cycle").innerHTML = ("Negative Duty Cycle: " + neg_duty.toString());
            }
            else if (measList[i] === "Falling_Count") {
                document.getElementById("Falling_Count").innerHTML = ("Falling Count: " + falling_cnt.toString());
            }
        }
        console.log(msg.ch1.meas.toString());
        xAxis.renderer.ticks.template.disabled = false;
        xAxis.renderer.ticks.template.strokeOpacity = 1;
        //xAxis.renderer.ticks.template.stroke = am4core.color("#495C43");
        xAxis.renderer.ticks.template.strokeWidth = 2;
        xAxis.renderer.ticks.template.length = 10;
        yAxis.renderer.ticks.template.disabled = false;
        yAxis.renderer.ticks.template.strokeOpacity = 1;
        //yAxis.renderer.ticks.template.stroke = am4core.color("#495C43");
        yAxis.renderer.ticks.template.strokeWidth = 2;
        yAxis.renderer.ticks.template.length = 10;
        var i = 0;
        var datum = [];
        var cursorX1 = parseFloat(document.getElementById("X1").value);
        var cursorX2 = parseFloat(document.getElementById("X2").value);
        var cursorY1 = parseFloat(document.getElementById("Y1").value);
        var cursorY2 = parseFloat(document.getElementById("Y2").value);
        var trigga = parseFloat(document.getElementById("Trigger").value);
        var xcursor_max = yAxis.max;
        var xcursor_min = yAxis.min;
        var ycursor_max = xAxis.max;
        var ycursor_min = xAxis.min;
        var trigga_max = xAxis.max;
        var trigga_min = xAxis.min;
        var y_cursor_times_1 = [ycursor_min, ycursor_max];
        var y_cursor_times_2 = [ycursor_min, ycursor_max];
        var x_cursor_times_1 = [cursorX1, cursorX1];
        var x_cursor_times_2 = [cursorX2, cursorX2];
        var y_cursor_volts_1 = [cursorY1, cursorY1];
        var y_cursor_volts_2 = [cursorY2, cursorY2];
        var x_cursor_volts_1 = [xcursor_max, xcursor_min];
        var x_cursor_volts_2 = [xcursor_max, xcursor_min];
        var trigga_times = [trigga_min, trigga_max];
        var trigga_volts = [trigga, trigga]
        document.getElementById("time_width").setAttribute("value", (h_scale).toString());
        document.getElementById("volt_width").setAttribute("value", (v_scale).toString());

        for (i = 0; i < ch1_vals.length; i++) {
            if (i < x_cursor_times_1.length) {
                datum.push({
                    'time': parseFloat(time_vals[i]), 'value': parseFloat(ch1_vals[i]),
                    'timeXC1': parseFloat(x_cursor_times_1[i]), 'valueXC1': parseFloat(x_cursor_volts_1[i]),
                    'timeXC2': parseFloat(x_cursor_times_2[i]), 'valueXC2': parseFloat(x_cursor_volts_2[i]),
                    'valueYC1': parseFloat(y_cursor_volts_1[i]), 'timeYC1': parseFloat(y_cursor_times_1[i]),
                    'valueYC2': parseFloat(y_cursor_volts_2[i]), 'timeYC2': parseFloat(y_cursor_times_2[i]),
                    'valueTrigga':parseFloat(trigga_volts[i]),'timeTrigga':parseFloat(trigga_times[i])
                });
            } else {
                datum.push({'time': Number(time_vals[i]), 'value': Number(ch1_vals[i])});
            }
        }


        //console.log(JSON.stringify(datum));
        chart.data = datum;
        //xAxis.min = xAxis.min + 1;
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

    $('form#start_form').submit(function(event) {
        socket.emit('bussy', {data: 'poopy'});
        console.log("You're a poopyhead");
        return false;
    });

    $('form#stop_form').submit(function(event) {
        socket.emit('bussy', {data: 'head'});
        console.log("You're a poopyhead");
        return false;
    });

    $('form#hscales').submit(function(event) {
        var h_scale = document.getElementById('hscale').value;
        console.log(h_scale);
/*        var v_scale = document.getElementById('vscale')
        console.log(v_scale);*/
        socket.emit('scales', {data: ['hageman', h_scale]});
        console.log("You're a poopyhead");
        return false;
    });
    $('form#vscales').submit(function(event) {
        var v_scale = document.getElementById('vscale').value;
        console.log(v_scale);
        socket.emit('scales', {data: ['bussy', v_scale]});
        console.log("You're a poopyhead");
        return false;
    });
    $('form#remmeas').submit(function(event) {
        var measurement = document.getElementById('measSelect').value;
        console.log(measurement);
        if (check_if_meas_exists(measurement, measList)) {
            var measList2 = [];
            for (var i=0; i<measList.length; i++) {
                if (measurement !== measList[i]) {
                    measList2.push(measList[i]);
                }
                else {
                    var ul = document.getElementById("measure_list");
                    var item = document.getElementById(measurement
                    );
                    ul.removeChild(item);

                }
            }

            measList = measList2;
            console.log(measList);
        }
        return false;
    });
    $('form#addmeas').submit(function(event) {
        var measurement = document.getElementById('measSelect').value;
        console.log(measurement);
        if (!check_if_meas_exists(measurement, measList)) {
            measList.push(measurement);
            console.log(measList);
            var ul = document.getElementById("measure_list");
            var li = document.createElement("li");
            li.setAttribute('id',measurement);
            li.appendChild(document.createTextNode(measurement));
            ul.appendChild(li);
        }
        return false;
    });
    $('form#cursor_form').submit(function(event) {
        console.log("Owo did you click me dadee?");
        var cursor = document.getElementById('cursor_select').value;
        var cursorX1 = parseFloat(document.getElementById("X1").value);
        var cursorX2 = parseFloat(document.getElementById("X2").value);
        var cursorY1 = parseFloat(document.getElementById("Y1").value);
        var cursorY2 = parseFloat(document.getElementById("Y2").value);
        var trigga = parseFloat(document.getElementById("Trigger").value);

        if (cursor === "X1") {
            cursorX1 = parseFloat(document.getElementById("X1").value);
        }
        else if (cursor === "X2") {
            cursorX2 = parseFloat(document.getElementById("X2").value);
        }
        else if (cursor === "Y1") {
            cursorY1 = parseFloat(document.getElementById("Y1").value);
        }
        else if (cursor === "Y2") {
            cursorY2 = parseFloat(document.getElementById("Y2").value);
        }
        else {//Trigger
            trigga = parseFloat(document.getElementById("Trigger").value);
        }
        socket.emit('cursors',{data: [cursorX1,cursorX2,cursorY1,cursorY2,trigga]});
        console.log("Sent my load uwu");
        return false;
    });
    $('form#hoffset_form').submit(function(event) {
        socket.emit('offset', {data: ['horizontal', document.getElementById('hoffset').value]});
        //console.log(cursor);

        return false;
    });
    $('form#voffset_form').submit(function(event) {
        //var cursor = document.getElementById('cursor_select').value;
        //console.log(cursor);
        socket.emit('offset', {data: ['vertical', document.getElementById('voffset').value]});
        return false;
    });
}

function check_if_meas_exists(measurement, measList) {
    for(var i=0; i<measList.length; i++) {
        if (measurement === measList[i]) {
            return true;
        }
    }
    return false;
}

function change_cursor_sel() {
    var cursor = document.getElementById("cursor_select").value;
    console.log("Cursor:" + cursor);
    var orig_val = document.getElementById("cursor_val").value;
    console.log("Orig Val:" + orig_val);
    var old_cursor = document.getElementById("old_cursor").value;
    console.log("Old Cursor:" + old_cursor);
    var cursor_val;
    if(cursor === "X1") {
        cursor_val = document.getElementById("X1").value;
    }
    else if (cursor === "X2") {
        cursor_val = document.getElementById("X2").value;
    }
    else if (cursor === "Y1") {
        cursor_val = document.getElementById("Y1").value;
    }
    else if (cursor === "Y2") {
        cursor_val = document.getElementById("Y2").value;
    }
    else {//Trigger
        cursor_val = document.getElementById("Trigger").value;
    }
    if(old_cursor === "X1") {
        document.getElementById("X1").setAttribute("value",orig_val);
    }
    else if (old_cursor === "X2") {
        document.getElementById("X2").setAttribute("value",orig_val);
    }
    else if (old_cursor === "Y1") {
        document.getElementById("Y1").setAttribute("value",orig_val);
    }
    else if (old_cursor === "Y2") {
        document.getElementById("Y2").setAttribute("value",orig_val);
    }
    else {//Trigger
        document.getElementById("Trigger").setAttribute("value",orig_val);
    }
    document.getElementById("cursor_val").setAttribute("value",cursor_val);
    document.getElementById("old_cursor").setAttribute("value",cursor);

}
function change_cursor_val(amount) {
    var cursor = document.getElementById("cursor_select").value;
    var width;
    if (cursor === "Y1" || cursor === "Y2") {
        width = parseFloat(document.getElementById("volt_width").value);
    }
    else if (cursor === "X1" || cursor === "X2") {
        width = parseFloat(document.getElementById("time_width").value);
    }
    else {
        width = parseFloat(document.getElementById("volt_width").value);
    }
    var change = (1/amount) * width;
    var original = parseFloat(document.getElementById("cursor_val").value);
    var not_original = original+change;
    if (not_original >= width/2) {
        not_original = width/2;
    }
    else if (not_original <= -width/2) {
        not_original = -width/2;
    }
    document.getElementById("cursor_val").setAttribute("value",(not_original).toString());
    if(cursor === "X1") {
        document.getElementById("X1").setAttribute("value",(not_original).toString());
    }
    else if (cursor === "X2") {
        document.getElementById("X2").setAttribute("value",(not_original).toString());
    }
    else if (cursor === "Y1") {
        document.getElementById("Y1").setAttribute("value",(not_original).toString());
    }
    else if (cursor === "Y2") {
        document.getElementById("Y2").setAttribute("value",(not_original).toString());;
    }
    else {
        document.getElementById("Trigger").setAttribute("value",(not_original).toString());
    }
}
