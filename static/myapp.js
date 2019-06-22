$(function () {
    var all_data;
    $.get("/api/test").done(function(data) {
        all_data = data;

        // create table
        html = "<tr>";
        daily_data = all_data["data"]
        for (var i=0; i<daily_data.length; i++) {
            str = `<td>
                        <div id="${"day"+i}" class="avatar" data-poptext="${daily_data[i]["winner"]["sub"] + " subs, " 
                                                                        + daily_data[i]["winner"]["solved"] + " solved on " + daily_data[i]["date"] + "."}">
                            <img src="${all_data["users"][daily_data[i]["winner"]["username"]]["avatar"]}" alt="avatar">
                        </div>
                    </td>`
            if((i+1) % 7 == 0) {
                str += '</tr><tr>'
            }
            html += str
        }
        html += "</tr>"
        $("table > tbody").append(html)

        // echarts part
        var option = {
            tooltip : {
                trigger: "axis",
                axisPointer : {           
                    type : "shadow"        
                }
            },
            legend: {
                data:["sub", "solved"]
            },
            grid: {
                left: "3%",
                right: "4%",
                bottom: "3%",
                containLabel: true
            },
            xAxis : [
                {
                    type : "category",
                    data : all_data["username_arr"]
                }
            ],
            yAxis : [
                {
                    type : "value"
                }
            ],
            series : [
                {
                    name:"solved",
                    type:"bar",
                    stack: "solved",
                    data: all_data["data"][all_data["data"].length - 1]["all_users"]["solved"],
                    itemStyle: {
                        normal: {
                            color: "#ABDDA4"
                        }
                    }
                },
                {
                    name:"sub",
                    type:"bar",
                    stack: "sub",
                    data:all_data["data"][all_data["data"].length - 1]["all_users"]["sub"],
                    itemStyle: {
                        normal: {
                            color: "#3288BD"
                        }
                    }
                },
            ]
        };

        var myChart = echarts.init(document.getElementById("oneday_stat_chart"));
        myChart.setOption(option);

        // click part
        $(".avatar").click(function() {
            var day_idx = parseInt($(this).attr("id").substr(3));
            myChart.setOption({
                series : [
                    {
                        name: "solved",
                        data: all_data["data"][day_idx]["all_users"]["solved"],
                    },
                    {
                        name:"sub",
                        data:all_data["data"][day_idx]["all_users"]["sub"],
                    },
                ]
            });
        });
    })
    

})