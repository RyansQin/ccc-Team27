import Vue from 'vue';
import App from './App.vue';
import echarts from 'echarts';
import VueRouter from 'vue-router';
import  {routes}  from './router';
import store from './store/store';
import VueResource from 'vue-resource';
//import axios from 'axios';
//import VueAxios from 'vue-axios';

Vue.use(echarts);
Vue.use(VueRouter);
//Vue.use(VueAxios,axios);
Vue.use(VueResource);

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
