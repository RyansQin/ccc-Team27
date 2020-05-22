<template>
    <div class="container">
        <app-header></app-header>
  <hr>
  <div class="map">
    
   
      <Stocks></Stocks>
   
    
  </div>
</div>
  
</template>

<script type="text/babel">
  import IEcharts from 'vue-echarts-v3/src/full.js';
  import PieChart from './portfolio/PieChart.vue';
  import Header from './Header.vue';
  import Stocks from '../components/stocks/map.vue';

  export default {
    components: {
      IEcharts,
      PieChart,
      appHeader: Header,
      Stocks
    },
    mounted: () => {
        console.log("testting");
        console.log(this);
    },
  };
</script>

<style >
 
       


</style>