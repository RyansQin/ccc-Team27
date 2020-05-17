import Home from './components/Home.vue'
import Details from './components/details/detailForState.vue'
import Stocks from "./components/stocks/map.vue";
import Welcome from "./components/Welcome.vue";

export const routes = [
    {path: '/', component: Welcome},
    {path: '/home', component: Home},
    {path: '/details', component: Details},
    {path: '/map', component: Stocks}


];