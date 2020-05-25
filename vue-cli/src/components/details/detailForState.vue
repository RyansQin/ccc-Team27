<template>
    <div>
        <Header></Header>    
    <hr>
    <div class="tweet1">Tweets Collected</div>
    <br>
    <div class="tweet2">The pie chart shows the number of tweets collected and the number of tweets that mention about COVID-19</div>
    <hr>
    <div class="col">
       <PieChart></PieChart>
    </div>
    <hr>
    <div class="sentiment1">Sentiment Analysis</div>
    <br>
    <div class="sentiment2">The pie chart shows the sentiment of people about COVID-19</div>
    <hr>
    <div class="col">
        <pieChartForSent></pieChartForSent>
    </div>
  
    <hr>
    <div class="title">Comparison between infection number and the number of concerned tweets</div>
    <hr>
    <div class="row">
    <div class="col">
       <LineChart></LineChart>
    </div>

    <div class="col">
       <lineChartForCovid></lineChartForCovid>
    </div>
    
  </div>
  <hr>
    <div class='actions'>What are people concerned about during lockdown</div>
    <hr>
    <div class="dowhat">
    <font-awesome-icon class="A" :icon="getA()" size="6x" :style="{color:'#74c476'}" />
    <div class="A"></div>
    <font-awesome-icon :icon="getB()" size="6x" :style="{color:'#810f7c'}" />
    <font-awesome-icon :icon="getC()" size="6x" :style="{color:'#fed976'}" />
    <!-- <i data-feather="film" color="#9e9ac8" width="100px" height="100px"></i>
    
    <i data-feather="tv" color="#6a51a3" width="100px" height="100px"></i>
    <i data-feather="book-open" color="#3f007d" width="100px" height="100px"></i>
    <i data-feather="video" color="#6a51a3" width="100px" height="100px"></i>
    <i data-feather="briefcase" color="#9e9ac8" width="100px" height="100px"></i> -->
    </div>
       

    </div>
</template>

<script>
 import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faChild } from '@fortawesome/free-solid-svg-icons'
import { faHouseUser } from '@fortawesome/free-solid-svg-icons'
import { faViruses } from '@fortawesome/free-solid-svg-icons'
import { faSchool } from '@fortawesome/free-solid-svg-icons'
import { faNewspaper } from '@fortawesome/free-solid-svg-icons'
import { faBriefcase } from '@fortawesome/free-solid-svg-icons'
import { faUserFriends } from '@fortawesome/free-solid-svg-icons'
import { faVideo } from '@fortawesome/free-solid-svg-icons'
import { faBookReader } from '@fortawesome/free-solid-svg-icons'
import { faFilm } from '@fortawesome/free-solid-svg-icons'
import { faGamepad } from '@fortawesome/free-solid-svg-icons'
import { faSuitcaseRolling } from '@fortawesome/free-solid-svg-icons'
  import Header from '../Header.vue';
  import PieChart from '../portfolio/PieChart.vue';
  import LineChart from '../lineChart/lineChart.vue';
  import lineChartForCovid from '../lineChart/lineChartForCovid.vue';
  import pieChartForSent from '../portfolio/PieChartForSent.vue';
export default {
    
    components: {
    
        Header,
        PieChart,
        LineChart,
        lineChartForCovid,
        pieChartForSent,
        FontAwesomeIcon
    },
    mounted: () => {
      feather.replace();
    },
    computed: {
        actionData() {
            
            return this.$store.getters.getAction;
        }
    },
    methods: {
        getA(){
            return this.getResult(this.actionData[0]);
        },
        getB(){
             return this.getResult(this.actionData[1]);
        },
        getC(){
            return this.getResult(this.actionData[2]);
        },

        getResult(action){
            if(action == 'child' || action == 'kid'){
                return faChild;
            }
            if(action == 'family'){
                return faHouseUser;
            }
            if(action == 'school'){
                return faSchool;
            }
            if(action == 'news'){
                return faNewspaper;
            }
            if(action == 'work'){
                return faBriefcase;
            }
            if(action == 'friend'){
                return faUserFriends;
            }
            if(action == 'video'){
                return faVideo;
            }
            if(action == 'read'){
                return faBookReader;
            }
            if(action == 'movie' || action =='film'){
                return faFilm;
            }
            if(action == 'virus'){
                return faViruses;
            }
            if(action == 'play'){
                return faGamepad;
            }
            if(action == 'travel'){
                return faSuitcaseRolling;
            }
        }

    }
}
</script>
<style>
.dowhat{
    text-align: center;
}
.A{
    width: 50px;
}
.title{
    text-align: center;
    font-size:3ch;
    
}
.tweet1{
    font-size: 3ch;
}

.tweet2{
    font-size: 1.5ch;
}

.sentiment1{
    font-size: 3ch;
}

.sentiment2{
    font-size: 1.5ch;
}

.actions{
    font-size: 3ch;
    text-align: center;
}
</style>