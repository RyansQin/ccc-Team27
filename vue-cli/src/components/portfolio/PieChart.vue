<template>

      <div id="pie_chart"></div>

</template>

<script>
  import echarts from 'echarts'
  export default {
    data() {
      return {
        covid: this.$store.getters.getCovidRate
      }
    },
    mounted() {
      console.log("piechart");
      console.log(this);
      this.buildPie();
    },
    methods: {
      buildPie() {
        let pie = echarts.init(document.getElementById('pie_chart'))
        let data = this.buildData()
        let option = {
          backgroundColor: '',
          title: {
            text: 'tweets collected',
            x: 'center',
            
          },
          tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}  {c} ({d}%)"
          },
          legend: {
            bottom: 10,
            left: 'center',
            data: data.labels
          },
          series: [{
            name: 'number',
            type: 'pie',
            radius: '55%',
            center: ['50%', '50%'],
            data: data.values,
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }]
        }

        pie.setOption(option)
        pie.on('click', function(params) {
          console.log(params.name, params.value, params.percent, params.seriesName, params.seriesType)
        })
      },
      buildData() {
        let labels = ['total','covid']
        let values = [];
        values.push({
          value: this.covid.total,
          name: labels[0],
          color: this.randomColor()
        }),
        values.push({
          value: this.covid.covid,
          name: labels[1],
          color: this.randomColor()
        })
        // for (let i = 0; i < labels.length; i++) {
        //   values.push({
        //     value: parseInt(Math.random() * 10000),
        //     name: labels[i],
        //     color: this.randomColor()
        //   })
        // }

        return {
          labels,
          values
        }
      },
      randomColor() {
        var r = Math.floor(Math.random() * 256);
        var g = Math.floor(Math.random() * 256);
        var b = Math.floor(Math.random() * 256);
        var color = '#' + r.toString(16) + g.toString(16) + b.toString(16);
        return color;
      }
    }
  }
</script>

<style scoped>
  #pie_chart {
    width: 500px;
    height: 400px;
  }
</style>
