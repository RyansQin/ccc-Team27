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
        allData() {
            
            return this.$store.getters.getDisease;
        },
        stateData() {
            
            return this.$store.getters.getStates;
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
        that.bar = {
          title:{
              text: 'Asthma',
              left: 'center',
                         textStyle:{
                  color:'#dd3497'
              }
          },
          tooltip:{},
          xAxis: {
            type: 'value',
          },
          yAxis: {
            type: 'category',
            data: this.stateData[0]
          },
          series: [
            {
              name: 'proportion',
              type: 'bar',
              itemStyle: {
                normal: {
                  color: new echarts.graphic.LinearGradient(
                    0, 0, 1, 0,
                    [
                      {offset: 0, color: '#fa9fb5'},
                      {offset: 0.5, color: '#dd3497'},
                      {offset: 1, color: '#7a0177'}
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
              data: [this.allData[8][1][0][1],this.allData[1][1][0][1],this.allData[6][1][0][1],this.allData[5][1][0][1],
              this.allData[2][1][0][1],this.allData[4][1][0][1],this.allData[7][1][0][1],this.allData[3][1][0][1]]
            }
          ]
        }
      }
    },
    // beforeMount () {
    //   const that = this
    // },
    mounted () {
    }
    // beforeDestroy () {
    //   const that = this
    // }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .echarts {
    width: 350px;
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
