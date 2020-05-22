<template>
  <div class="jumbotron jumbotron-fluid">
  <h1 class="display-3 text-secondary ">COVID_19</h1>
  <hr>
  <p class="display-4 text-muted shadow p-3 mb-5 rounded">what are people doing during lockdown</p>
  <hr class="my-4">

  <router-link to="/home" class="btn btn-primary btn-lg" ><a>Let's go</a></router-link>
</div>
</template>


<script>

export default {
   mounted: () => {
        console.log("testting");
        console.log(this);
        console.log(this.$store);
        
    }
  
}
</script>


<style scoped>
    .jumbotron{
        width: 100%;
        height: 100%;
        background-image: url('./picture/COVID_19_iS1210596217_hero.jpg');
        position: absolute;
        left: 0;
        top: 0;
        z-index: -1;
    }
    
</style>>