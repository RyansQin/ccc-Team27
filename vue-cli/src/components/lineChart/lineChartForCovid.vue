<template>
  <div class="echarts">
    <IEcharts
      :option="option"
      @ready="onReady"
    />
  </div>
</template>

<script>
  import IEcharts from 'vue-echarts-v3';
  const symbolSize = 20
  export default {
    name: 'Demo01',
    components: {
      IEcharts
    },
    data () {
      // const that = this
      return {
        ins: null,
        echarts: null,
        option: {},
        
      }
    },
    computed: {
        date() {
          return this.$store.getters.getDate;
        },
        covidData() {
          console.log("chekc chekc");
          console.log(this.$store.getters.getDailyCovid);
            return this.$store.getters.getDailyCovid;
        }
    },
    methods: {
      onReady (instance, echarts) {
        const that = this
        that.ins = instance
        that.echarts = echarts
        that.option =  {
          title: {
            text: 'the number of infections',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          grid: {
          },
          legend: {
            data: ['infected number']
          },
          yAxis: {
            name: '',
                nameTextStyle: {
                    color: '#FA6F53',
                    fontSize: 16,
                    padding: [0, 0, 10, 0]
                },
                
                type: 'value'
          },
          xAxis: {
            type: 'category',
                boundaryGap: false,     //坐标轴两边不留白
                data: this.date,
                name: '', //X轴 name
                nameTextStyle: {        //坐标轴名称的文字样式
                    color: '#FA6F53',
                    fontSize: 16,
                    padding: [0, 0, 0, 20]
                },
                
          },
        //   dataZoom: [
        //     {
        //       type: 'slider',
        //       xAxisIndex: 0,
        //       filterMode: 'empty'
        //     },
        //     {
        //       type: 'slider',
        //       yAxisIndex: 0,
        //       filterMode: 'empty'
        //     },
        //     {
        //       type: 'inside',
        //       xAxisIndex: 0,
        //       filterMode: 'empty'
        //     },
        //     {
        //       type: 'inside',
        //       yAxisIndex: 0,
        //       filterMode: 'empty'
        //     }
        //   ],
          series: [

            {
              
              type: 'line',
              smooth: false,
              lineStyle: {                // 线条样式 => 必须使用normal属性
                    normal: {
                        color: '#000000',
                    }
                },
              data: this.covidData
            }
          ]
        }
    }
  }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .echarts {
    width: 500px;
    height: 400px;
    margin: 0 auto;
  }
  h1, h2 {
    font-weight: normal;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: inline-block;
    margin: 0 10px;
  }
  a {
    color: #42b983;
  }
</style>
