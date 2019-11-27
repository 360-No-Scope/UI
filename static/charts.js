function initChart() {
    var chart = am4core.create(document.getElementById("amChart"), am4charts.XYChart);
    var timeAxis = chart.xAxes.push(new am4charts.ValueAxis());
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.max = 1;
    valueAxis.min = -1;
    valueAxis.title.text = "Volts (V)";
    //timeAxis.strictMinMax = true;
    timeAxis.max = .5;
    timeAxis.min = -.5;
    timeAxis.title.text = "Time (s)";

    var series = chart.series.push(new am4charts.LineSeries());
    series.name = "Channel 1";
    series.dataFields.valueY = "value";
    series.dataFields.valueX = "time";
    series.fill = am4core.color("#265c98");
    series.stroke = am4core.color("#265c98");

    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.valueX = "timeXC1";
    series2.dataFields.valueY = "valueXC1";
    series2.name = "Cursor X1";
    series2.fill = am4core.color("#91507b");
    series2.stroke = am4core.color("#91507b");

    var series3 = chart.series.push(new am4charts.LineSeries());
    series3.dataFields.valueX = "timeYC1";
    series3.dataFields.valueY = "valueYC1";
    series3.name = "Cursor Y1";
    series3.fill = am4core.color("#8f623b");
    series3.stroke = am4core.color("#8f623b");

    var series4 = chart.series.push(new am4charts.LineSeries());
    series4.dataFields.valueX = "timeYC2";
    series4.dataFields.valueY = "valueYC2";
    series4.name = "Cursor Y2";
    series4.fill = am4core.color("#8f623b");
    series4.stroke = am4core.color("#8f623b");

    var series5 = chart.series.push(new am4charts.LineSeries());
    series5.dataFields.valueX = "timeXC2";
    series5.dataFields.valueY = "valueXC2";
    series5.name = "Cursor X2";
    series5.fill = am4core.color("#91507b");
    series5.stroke = am4core.color("#91507b");

    var series6 = chart.series.push(new am4charts.LineSeries());
    series6.dataFields.valueX = "timeTrigga";
    series6.dataFields.valueY = "valueTrigga";
    series6.name = "Trigger";
    series6.fill = am4core.color("#547839");
    series6.stroke = am4core.color("#547839");
/*    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.name = "Channel 2";
    series2.dataFields.valueY = "value2";
    series2.dataFields.valueX = "time";
    series2.stroke = am4core.color("red");*/


    // Add data
    //var chartdata = {'chart':chart, 'axes':[timeAxis,valueAxis], 'series'}
    // And, for a good measure, let's add a legend
    chart.legend = new am4charts.Legend();
    chart_data = {chart:chart, xAxis:timeAxis, yAxis:valueAxis}
    return chart_data

}

