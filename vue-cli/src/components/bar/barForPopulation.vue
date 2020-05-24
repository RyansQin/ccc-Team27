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
            
            return this.$store.getters.getPopulation;
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
                text:'population density',
                left: 'center',
                textStyle:{
                  color:'#807dba'
                }
            },
          tooltip:{},
          yAxis: {
            type: 'value',
          },
          xAxis: {
            type: 'category',
            data: this.stateData[0]
          },
          series: [
            {
                name:'popualtion_density',
              type: 'bar',
              itemStyle: {
                normal: {
                  color: new echarts.graphic.LinearGradient(
                    0, 0, 0, 1,
                    [
                      {offset: 0, color: '#bcbddc'},
                      {offset: 0.5, color: '#807dba'},
                      {offset: 1, color: '#54278f'}
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
              data: [this.allData[8][1],this.allData[1][1],this.allData[6][1],this.allData[5][1],
              this.allData[2][1],this.allData[4][1],this.allData[7][1],this.allData[3][1]]
            }
          ]
        }
      }
    },
    // beforeMount () {
    //   const that = this
    // },
    mounted () {
        console.log("population");
        console.log(this.$store.getters.getPopulation);
    }
    // beforeDestroy () {
    //   const that = this
    // }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .echarts {
    width: 800px;
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
