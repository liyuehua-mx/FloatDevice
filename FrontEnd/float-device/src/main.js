
import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';

Vue.config.productionTip = false
import axios from 'axios'          //引入axios

Vue.prototype.$axios = axios;      //把axios挂载到vue上
Vue.use(ElementUI);

new Vue({
  el: '#app',
  render: h => h(App)
});