import Vue from 'vue'

Vue.config.productionTip = false

import * as VueGoogleMaps from 'vue2-google-maps'
Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyAqQVoMDzkiNOVGg_r_gfirxBfDq6A9GmA'
  }
})
