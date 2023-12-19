import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import i18n from './i18n'
import './services/rest/base'
import './styles/custom.scss'
import "@fortawesome/fontawesome-free/css/all.css"
import ClickOutside from '@/directives/ClickOutside'
import './registerServiceWorker'

createApp(App)
    .use(store)
    .use(router)
    .use(i18n)
    .directive("click-outside", ClickOutside)
    .mount('#app')
