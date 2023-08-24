import './index.css'

import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import CKEditor from '@ckeditor/ckeditor5-vue';
// import CKEditor from 'ckeditor5-custom-build/build/ckeditor';
import { Button, setConfig, frappeRequest, resourcesPlugin } from 'frappe-ui'

let app = createApp(App)

setConfig('resourceFetcher', frappeRequest)

app.use(router)
app.use(resourcesPlugin)
app.use(CKEditor)

app.component('Button', Button)
app.mount('#app')
