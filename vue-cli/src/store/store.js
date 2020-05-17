import Vue from 'vue';
import Vuex from 'vuex';

import map from './map';
import details from './details';

import * as actions from './actions';

Vue.use(Vuex);

export default new Vuex.Store({
    actions,
    modules: {
    map,
    details
    }
});