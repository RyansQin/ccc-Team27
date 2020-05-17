<template>
  <div class="echarts">
    
    <IEcharts
      :option="bar"
      @ready="onReady"
    />
  </div>
</template>

<script>
  import IEcharts from 'vue-echarts-v3'

  export default {
    name: 'Demo03',
    components: {
      IEcharts
    },
    data () {
      // const that = this
      return {
        ins: null,
        echarts: null,
        bar: {},
      }
    },
    computed: {
        covidData() {
            
            return this.$store.getters.getCovidRate;
        }
    },
    // created() {
    //         this.$store.dispatch('initCovidRate')
    //     },
    methods: {
      onReady (instance, echarts) {
        
        const that = this
        that.ins = instance
        that.echarts = echarts
        var data1 = this.covidData.covid
        //console.log(data1 + "zxczxczxc")
        var data2 = this.covidData.total
        that.bar = {
          xAxis: {
            data: ['covid', 'total'],
            axisLabel: {
              inside: false,
              textStyle: {
                interval: 0,
                color: '#000000',
                fontSize: 12
              }
            },
            axisTick: {
              show: true
            },
            axisLine: {
              show: true
            },
            z: 10
          },
          yAxis: {
            axisLine: {
              show: true
            },
            axisTick: {
              show: true
            },
            axisLabel: {
              textStyle: {
                color: '#000000'
              }
            }
          },
          dataZoom: [
            {
              type: 'inside'
            }
          ],
          series: [
            {
              type: 'bar',
              itemStyle: {
                normal: {
                  color: new echarts.graphic.LinearGradient(
                    0, 0, 0, 1,
                    [
                      {offset: 0, color: '#83bff6'},
                      {offset: 0.5, color: '#188df0'},
                      {offset: 1, color: '#188df0'}
                    ]
                  )
                }
              },
              label: {
                normal: {
                  fontWeight: 'bolder',
                  fontSize: 23
                }
              },
              barWidth: 20,
              data: [parseInt(data1), parseInt(data2)]
            }
          ]
        }
      }
    },
    // beforeMount () {
    //   const that = this
    // },
    mounted () {
       console.log("bar");
       console.log(this.$store.getters.getCovidRate);
    }
    // beforeDestroy () {
    //   const that = this
    // }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .echarts {
    width: 400px;
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
