function initChart() {
    var chart = am4core.create(document.getElementById("amChart"), am4charts.XYChart);
    var timeAxis = chart.xAxes.push(new am4charts.ValueAxis());
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.max = 7;
    valueAxis.min = -7;
    timeAxis.max = 10;
    timeAxis.min = -10;

    var series = chart.series.push(new am4charts.LineSeries());
    series.name = "Channel 1";
    series.dataFields.valueY = "value";
    series.dataFields.valueX = "time";


/*    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.name = "Channel 2";
    series2.dataFields.valueY = "value2";
    series2.dataFields.valueX = "time";
    series2.stroke = am4core.color("red");*/


    // Add data
    //var chartdata = {'chart':chart, 'axes':[timeAxis,valueAxis], 'series'}
    // And, for a good measure, let's add a legend
    chart.legend = new am4charts.Legend();
    return chart

}

