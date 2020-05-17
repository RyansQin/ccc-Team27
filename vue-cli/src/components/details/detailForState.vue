<template>
    <div>
        <Header></Header>
    <div class="row">
    <div class="col">
       <Bar></Bar>
    </div>
    <div class="col">
        <PieChart></PieChart>
    </div>
  </div>
       

    </div>
</template>

<script>
  import Bar from '../bar/bar';
  import Header from '../Header.vue';
  import PieChart from '../portfolio/PieChart.vue';

export default {
    components: {
        Bar,
        Header,
        PieChart
    },

    mounted: () => {
        console.log("yuting");
        console.log(this.$store);
    },
}
</script>