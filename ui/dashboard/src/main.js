import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './services/base';
import './styles/bulma.scss'
import './styles/custom.scss'
import "@fortawesome/fontawesome-free/css/all.css";
import ClickOutside from '@/directives/ClickOutside';
import './registerServiceWorker'

createApp(App)
    .use(store)
    .use(router)
    .directive("click-outside", ClickOutside)
    .mount('#app')
