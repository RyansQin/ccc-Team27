<template>
    <div>
        <Header></Header>    
    <hr>
    <div class="age_distribution">Age Distribution</div>
    <br>
    <div class="age_distribution1">the bar shows the proportion of people over 60 years old of eight regions in Australia. With increasing age, the probability of disease infection may also increase</div>
    <div class="age">
       <BarForAge></BarForAge>
    </div>
    <hr>
    <div class="population1">Population Density</div>
    <br>
    <div class="population2">the bar shows the population density of eight regions in Australia. 
The greater the population, the higher the probability of disease transmission</div>
    <div class="population">
        <BarForPopulation></BarForPopulation>
    </div>
    <hr>
    <div class="tourism1">Tourism</div>
    <br>
    <div class="tourism2">the bar shows the total number of tourists in one year of eight regions in Australia. The development of tourism represents the increase of foreign population</div>
    <div class="tourism">
        <BarForTourism></BarForTourism>
    </div>
    <hr>
    <div class="disease1">Diseases</div>
    <br>
    <div class="disease2">these five bars shows the incidence of five chronic diseases of eight regions in Australia.</div>
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
    },
}
</script>
<style>
.dowhat{
    text-align: center;
}
.title{
    text-align: center;
    font-size:4ch;
    
}
.age_distribution{
    font-size: 3ch;
    color: #4292c6;
}
.age_distribution1{
    
    color: #4292c6;
    font-size: 1.5ch;
}

.population1{
    font-size: 3ch;
    color: #807dba;
}
.population2{
    font-size: 1.5ch;
    color: #807dba
}
.tourism1{
    font-size: 3ch;
    color: #74c476
}
.tourism2{
    font-size: 1.5ch;
    color: #74c476
}

.disease1{
    font-size: 3ch;
    
}

.disease2{
    font-size: 1.5ch;
    
}
</style>