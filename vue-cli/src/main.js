import Vue from 'vue';
import App from './App.vue';
import echarts from 'echarts';
import VueRouter from 'vue-router';
import  {routes}  from './router';
import store from './store/store';
import VueResource from 'vue-resource';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faUserSecret } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
//import axios from 'axios';
//import VueAxios from 'vue-axios';
library.add(faUserSecret);
Vue.component('font-awesome-icon',FontAwesomeIcon);
Vue.use(echarts);
Vue.use(VueRouter);
//Vue.use(VueAxios,axios);
Vue.use(VueResource);
Vue.config.productionTip = false;
Vue.http.options.xhr = {withCredentials: true};
const router = new VueRouter({
  mode: 'history',
  routes
});

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
