<template>
<div>
    <div class="frame">
        <div style="position: relative; height: 10%; paddimg-right: 0.5em; width: 30%;">
            <ul>
                <li>
                   
                    <div class="one">aaaa</div>
                    <div style="display:inline; width:'50px'; height:'25px'">3082 cases</div>
                  
                    
                    
                </li>

                <li>
                    <div class="two">aaaa</div>
                    <div style="display:inline; width:'50px'; height:'25px'">1581 cases</div>
                </li>

                <li>
                    <div class="three">aaaa</div>
                    <div style="display:inline; width:'50px'; height:'25px'">1058 cases</div>
                </li>

                <li>
                    <div class="four">aaaa</div>
                    <div style="display:inline; width:'50px'; height:'25px'">557 cases</div>
                </li>


                <li>
                    <div class="five">aaaa</div>
                    <div style="display:inline; width:'50px'; height:'25px'">439 cases</div>
                </li>

                <li>
                   <div class="six">aaaa</div>
                    <div style="display:inline; width:'50px'; height:'25px'">226 cases</div>
                </li>

                <li>
                   <div class="seven">aaaa</div>
                    <div style="display:inline; width:'50px'; height:'25px'">107 cases</div>
                </li>

                <li>
                    <div class="eight">aaaa</div>
                    <div style="display:inline; width:'50px'; height:'25px'">30 cases</div>
                </li>

            </ul>
        </div>
        <div class="row">
        <div class="col">
            <div class="map" ref="myEchart"></div>
        </div>
        <div  class="col">
            <Bar></Bar>
        </div>
        </div>
        
    </div>
</div>
</template>

<script>
import echarts from 'echarts';
import aus from './states.json';
import Bar from '../bar/bar.vue';
var myJson = aus;


export default {
    components: {
        Bar
    },
    props: {
        areaCode: {
            type: String,
            default: "22"
        },
        max: {
            type: String,
            default: '500'
        },
        height: {
            type: String,
            default: document.documentElement.clientHeight-320+ 'px'
        }
    },

    data() {
        return {
            location: '',
            chart: null,
            chartData: [],
            option: {
                title : {
                    left: 'center',
                    textStyle:{
                        fontSize:16,
                    }
                }
            },
            
        }
    },
    computed: {
        colors() {
            return this.$store.getters.getAllColors;
        }
    },

   mounted() {
       this.initChart();
    },
    created() {
        this.$store.dispatch('initColors');
    },
    methods: {
        nameTransfer(location){
            switch(location){
                case "Western Australia":
                    return "per";
                case "Northern Territory":
                    return "nor";
                case "Queensland":
                    return "que";
                case "South Australia":
                    return "ade";
                case "New South Wales":
                    return "nsw";
                case "Australian Capital Territory":
                    return "can";
                case  "Victoria":
                    return "vic";
                case  "Tasmania":
                    return "tas";
              }
        },
        initData(location, self) {
            var task1 = 'covidRate';
            var task2 = 'curve';
            var task3 = 'lockdown';
            var loca = self.nameTransfer(location);
            var covidRateInfo = {};
            var curve = [];
            var sentiment = [];
            self.$http.get('http://172.26.131.203:8000/view/'+ task1+ '/'+ loca)
            .then(response => response.json())
            .then(data => {
                if(data){
                    covidRateInfo = {
                        covidRate: data.covidRate,
                        location: self.location
                    };
                    self.$http.get('http://172.26.131.203:8000/view/'+ task2+ '/'+ loca)
                    .then(response => response.json())
                    .then(data => {
                        if(data){
                        curve = data.curve[1];

                        self.$http.get('http://172.26.131.203:8000/view/'+ task3+ '/'+ loca)
                        .then(response => response.json())
                        .then(data => {
                        if(data){
                            sentiment = data.lockdownRank[1][1];
                            self.$store.dispatch('loadCovidRate',covidRateInfo);
                            self.$store.dispatch('loadCurve', curve);
                            self.$store.dispatch('loadDate', self.location);
                            self.$store.dispatch('loadSentiment',sentiment);
                            self.$router.push({path: '/details'}); 

                        }
                    });
                        };

                    })
                }
            })
            // self.$http.get('http://172.26.131.203:8000/view/${task2}/${loca}')
            // .then(response => response.json())
            // .then(data => {
            //     if(data){
            //         curve = data.curve[1];
            //     }
            // })
            //  self.$http.get('http://172.26.131.203:8000/view/${task3}/${loca}')
            // .then(response => response.json())
            // .then(data => {
            //     if(data){
            //         sentiment = data.lockdownRank[1][1];
            //         self.$store.dispatch('loadCovidRate',covidRateInfo);
            //         self.$store.dispatch('loadCurve', curve);
            //         self.$store.dispatch('loadDate', self.location);
            //         self.$store.dispatch('loadSentiment',sentiment);
            //         self.$router.push({path: '/details'}); 
            //     }
            // });


            // var request = {
	        //     "task":{
		    //     "location": self.nameTransfer(location),
		    //     "covid": true,
            //     "lockdown": true,
            //     "curve": true
	        //     }
            //     }
            // console.log(request);
            // self.$http.post('http://172.26.131.203:8000/view',request)
            // .then(response => response.json())
            // .then(data => {
            //     if(data){
            //         // var location = request.location;
            //         // var covid = data.covidRate;
            //         var covidRateInfo = {
            //             covidRate: data.covidRate,
            //             location: self.location

            //         }
            //         var curve = data.curve[1];
            //         var sentiment = data.lockdownRank[1][1];
            //         self.$store.dispatch('loadCovidRate',covidRateInfo);
            //         self.$store.dispatch('loadCurve', curve);
            //         self.$store.dispatch('loadDate', self.location);
            //         self.$store.dispatch('loadSentiment',sentiment);
            //         self.$router.push({path: '/details'}); 
            //     }
            // });
            
        },

        initChart() {// 初始化
            var self = this;
            this.chart = echarts.init(this.$refs.myEchart);
            this.getAreaMapInfoList();

            this.chart.on('click', function (params) {
                self.location = params.name;
                self.$options.methods.initData(self.location,self);
                
            });
            
        },
        getAreaMapInfoList () {// 获取地图数据
            for( var i=0;i<myJson.features.length;i++ ){
                let name = myJson.features[i].properties.name;
                let code = myJson.features[i].properties.code;     
                this.chartData.push({
                    name: name,
                    code: code
                });
            }
            //注册地图
            echarts.registerMap('australia', myJson);
           this.renderMap('australia',this.chartData);
        },
        renderMap(map,data){ //绘制地图
            this.option.title.subtext = "";
             //地理坐标系组件
            this.option.geo = {//引入地图 ，渲染地图凹凸显示
                    map: map,
                label: {
                        normal: {
                            show: true,
                            color: '#000000'
                        },
                        emphasis: {
                            show: false,
                            color: '#fff'
                        }
                    },
                roam: true,//禁止缩放
                zoom: 1,
                itemStyle: {
                    normal: {
                        borderColor: '#387ba7',//地图边界线的颜色
                        areaColor: '#1c3c63',//地图整体区域的颜色
                        shadowColor: 'rgba(0, 0, 0, 0.5)',
                        shadowBlur: 10,
                        shadowOffsetX: 10
                    },
                    emphasis: {
                        areaColor: '#132845'//鼠标滑过的颜色
                    }
                },
                regions: [
                {
                    name: 'New South Wales',
                    itemStyle: {
                        normal: {
                            areaColor: this.colors[0].color
                        },
                    }
                },
                {
                    name: 'Victoria',
                    itemStyle: {
                        normal: {
                            areaColor: this.colors[1].color
                        },
                    }
                },                
                {
                    name: 'Queensland',
                    itemStyle: {
                        normal: {
                            areaColor: this.colors[2].color
                        },
                    }
                },                    
                {
                    name: 'South Australia',
                    itemStyle: {
                        normal: {
                            areaColor: this.colors[4].color
                        },
                    }
                },
                {
                    name: 'Western Australia',
                    itemStyle: {
                        normal: {
                            areaColor: this.colors[3].color
                        },
                    }
                },
                {
                    name: 'Tasmania',
                    itemStyle: {
                        normal: {
                            areaColor: this.colors[5].color
                        },
                    }
                },
                {
                    name: 'Australian Capital Territory',
                    itemStyle: {
                        normal: {
                            areaColor: this.colors[6].color
                        },
                    }
                },
                {
                    name: 'Northern Territory',
                    itemStyle: {
                        normal: {
                            areaColor: this.colors[7].color
                        },
                    }
                },
                ]
                },
                
                // 地图标点
            this.option.series = [
             {
                    name: 'point',
                    type: 'scatter',
                    coordinateSystem: 'geo',
                    symbol: 'pin', //关系图节点标记的图形
                    symbolSize: [30, 30],
                    symbolOffset: [0, '-40%'],//关系图节点标记相对于原本位置的偏移。[0, '50%']
                    large : true,
                    label: {
                        normal: {
                            show: true,
                            textStyle: {
                                color: '#fff',
                                fontSize: 9,
                            }
                        }
                    },
            
                    itemStyle : {//===============图形样式，有 normal 和 emphasis 两个状态。normal 是图形在默认状态下的样式；emphasis 是图形在高亮状态下的样式，比如在鼠标悬浮或者图例联动高亮时。
                        normal : { //默认样式
                            label : {
                                show : true
                            },
                            borderType : 'solid', //图形描边类型，默认为实线，支持 'solid'（实线）, 'dashed'(虚线), 'dotted'（点线）。
                            borderColor : 'rgba(255,215,0,0.4)', //设置图形边框为淡金色,透明度为0.4
                            borderWidth : 2, //图形的描边线宽。为 0 时无描边。
                            opacity : 1
                        // 图形透明度。支持从 0 到 1 的数字，为 0 时不绘制该图形。默认0.5

                        },
                        emphasis : {//高亮状态

                        }
                    },
                    lineStyle : { //==========关系边的公用线条样式。
                        normal : {
                            color : 'rgba(255,0,255,0.4)',
                            width : '3',
                            type : 'dotted', //线的类型 'solid'（实线）'dashed'（虚线）'dotted'（点线）
                            curveness : 0.3, //线条的曲线程度，从0到1
                            opacity : 1
                        // 图形透明度。支持从 0 到 1 的数字，为 0 时不绘制该图形。默认0.5
                        },
                        emphasis : {//高亮状态

                        }
                    },
                    label : { //=============图形上的文本标签
                        normal : {
                            show : true,//是否显示标签。
                            position : 'inside',//标签的位置。['50%', '50%'] [x,y]
                            textStyle : { //标签的字体样式
                                color : '#cde6c7', //字体颜色
                                fontStyle : 'normal',//文字字体的风格 'normal'标准 'italic'斜体 'oblique' 倾斜
                                fontWeight : 'bolder',//'normal'标准'bold'粗的'bolder'更粗的'lighter'更细的或100 | 200 | 300 | 400...
                                
                                fontSize : 12, //字体大小
                            }
                        },
                        emphasis : {//高亮状态

                        }
                    },
                    edgeLabel : {//==============线条的边缘标签 
                        normal : {
                            show : false
                        },
                        emphasis : {//高亮状态

                        }
                    },

                    zlevel: 12,
                    data: data,
                }
               
                
            ];
            //渲染地图
            this.chart.setOption(this.option);
        }
    }
}

// this.chart.on('click', function(param) {
//     var name = param;
//     alert("asd");
// });


</script>

<style scoped>
    /* .frame {
       width: 100%;
        height: 100%;
        background-image: url('../picture/COVID_19_iS1210596217_hero.jpg');
        z-index: -1;
    } */
    .map {
        width: 600px;
        height: 521px;
    }
    .one {
        background-color: #67000d;
        display: inline;
        color: #67000d;
    }
       .two {
        background-color: #a50f15;
        display: inline;
        color: #a50f15;
    }
       .three {
        background-color: #cb181d;
        display: inline;
        color: #cb181d;
    }
       .four {
        background-color: #ef3b2c;
        display: inline;
        color: #ef3b2c;
    }
       .five {
        background-color: #fb6a4a;
        display: inline;
        color: #fb6a4a;
    }
       .six {
        background-color: #fc9272;
        display: inline;
        color: #fc9272;
    }
       .seven {
        background-color: #fcbba1;
        display: inline;
        color: #fcbba1;
    }
       .eight {
        background-color: #fee0d2;
        display: inline;
        color: #fee0d2;
    }

</style>

