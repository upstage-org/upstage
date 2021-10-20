import { createApp } from 'vue'
import { store, key } from './store'
import App from './App.vue'
import './styles/studio.less';

createApp(App).use(store, key).mount('#app')
