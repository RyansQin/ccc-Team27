<template>
   <nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="#">Lockdown</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li >
        
        <a class="nav-link" @click="toHome()" href="#">Home <span class="sr-only">(current)</span></a>
      </li>

      <li>
         <a class="nav-link" @click="loadAurin()" href="#">Aurin <span class="sr-only">(current)</span></a>
      </li>

      
    </ul>
  </div>
</nav>
</template>

<script>
import {mapActions} from 'vuex';
export default {
    methods: {
        ...mapActions({
            fetchData: 'loadData'
        }),

        loadData() {
            this.fetchData();
        },

        toHome() {
          this.$router.push({path: '/home'});
        },
        loadAurin(){
          var age = [];
          var population = [];
          var tourism = [];
          var disease = [];
          this.$http.get('http://172.26.131.203:8000/aurin/ageDistribution/60')
          .then(response=>response.json())
          .then(data => {
            if(data){
              age = data.result[0][1];
              this.$http.get('http://172.26.131.203:8000/aurin/population_density')
              .then(response => response.json())
              .then(data =>{
                if(data){
                  population = data.result[0];
                  this.$http.get('http://172.26.131.203:8000/aurin/tourism')
                  .then(response => response.json())
                  .then(data => {
                    if(data){
                      tourism = data.result[0];
                      this.$http.get('http://172.26.131.203:8000/aurin/disease')
                      .then(response => response.json())
                      .then(data =>{
                        disease = data.result[0];
                        this.$store.dispatch('loadAge',age);
                        this.$store.dispatch('loadPopulation', population);
                        this.$store.dispatch('loadTourism', tourism);
                        this.$store.dispatch('loadDisease', disease);
                        // self.$store.dispatch('loadSentiment',sentiment);
                        this.toAurin();
                      })
                    }
                  })
                }
              })

            }
          })

          // var request = {
	        //     "task": 
          //     ["age_distribution", "population_density", "tourism","disease"], "location": ["nor", "nsw", "vic", "can", "ade", "que", "tas", "per"],
	        //     "option":{"age1":60,"age2":null}
          //       }
          //   console.log(request);
          //   this.$http.post('http://172.26.131.203:8000/aurin',request)
          //   .then(response => response.json())
          //   .then(data => {
          //       if(data){
          //           // var location = request.location;
          //           // var covid = data.covidRate;
          //           var age = data.result[0][1];
          //           var population = data.result[1];
          //           var tourism = data.result[2];
          //           var disease = data.result[3];
          //           this.$store.dispatch('loadAge',age);
          //           this.$store.dispatch('loadPopulation', population);
          //           this.$store.dispatch('loadTourism', tourism);
          //           this.$store.dispatch('loadDisease', disease);
          //          // self.$store.dispatch('loadSentiment',sentiment);
          //           this.toAurin();
          //       }
          //   });
        },


        toAurin() {
          this.$router.push({path: '/aurin'});
        }

    }
}
</script>>