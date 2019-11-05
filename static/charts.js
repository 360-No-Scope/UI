function initChart() {
    var chart = am4core.create(document.getElementById("amChart"), am4charts.XYChart);
    var timeAxis = chart.xAxes.push(new am4charts.ValueAxis());
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.max = 7;
    valueAxis.min = -7;
    //timeAxis.strictMinMax = true;
    timeAxis.max = 10;
    timeAxis.min = -10;
    timeAxis.title.text = "Time (s)";

    var series = chart.series.push(new am4charts.LineSeries());
    series.name = "Channel 1";
    series.dataFields.valueY = "value";
    series.dataFields.valueX = "time";

    /*var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.valueX = "timeXC1";
    series2.dataFields.valueY = "valueXC1";
    series2.name = "Cursor X1";

    var series3 = chart.series.push(new am4charts.LineSeries());
    series3.dataFields.valueX = "timeYC1";
    series3.dataFields.valueY = "valueYC1";
    series3.name = "Cursor Y1";

    var series4 = chart.series.push(new am4charts.LineSeries());
    series4.dataFields.valueX = "timeYC2";
    series4.dataFields.valueY = "valueYC2";
    series4.name = "Cursor Y2";

    var series5 = chart.series.push(new am4charts.LineSeries());
    series5.dataFields.valueX = "timeXC2";
    series5.dataFields.valueY = "valueXC2";
    series5.name = "Cursor X2";*/
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

