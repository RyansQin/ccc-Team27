<template>
    <div>
        <Header></Header>    
    <hr>
    <div class="row">
    <div class="col-sm">
       <BarForAge></BarForAge>
    </div>
    <div class="col-sm">
        <BarForPopulation></BarForPopulation>
    </div>
    <div class="col-sm">
        <BarForTourism></BarForTourism>
    </div>
    </div>
    <hr>
    <div class="row">
    <div class="col">
       <BarForAsthma></BarForAsthma>
    </div>
    <div class="col">
        <BarForBlood></BarForBlood>
    </div>
    <div class="col">
        <BarForCirculatory></BarForCirculatory>
    </div>
    <div class="col">
        <BarForDiabete></BarForDiabete>
    </div>
    <div class="col">
        <BarForHeart></BarForHeart>
    </div>
    </div>

    </div>
</template>

<script>
  
  import Header from '../Header.vue';
  import BarForAge from '../bar/barForAge.vue';
  import BarForPopulation from '../bar/barForPopulation.vue';
  import BarForTourism from '../bar/barForTourism.vue';
  import BarForAsthma from '../bar/barForAsthma.vue';
  import BarForBlood from '../bar/barForBlood.vue';
  import BarForCirculatory from '../bar/barForCirculatory.vue';
  import BarForDiabete from '../bar/barForDiabete.vue';
  import BarForHeart from '../bar/barForHeart.vue';
  
export default {
    components: {
    
        Header,
        BarForAge,
        BarForPopulation,
        BarForTourism,
        BarForAsthma,
        BarForBlood,
        BarForCirculatory,
        BarForDiabete,
        BarForHeart
    },

    mounted: () => {
      feather.replace();
    },
}
</script>
<style>
.dowhat{
    text-align: center;
}
</style>