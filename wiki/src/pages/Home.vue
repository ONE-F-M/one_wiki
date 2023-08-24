<template>
  <Base>
    
  </Base>
</template>

<script>
import { Dialog } from 'frappe-ui'
import Base from './Base.vue'

export default {
  name: 'Home',
  data() {
    return {
      showDialog: false,
    }
  },
  mounted(){
    console.log('hi')
  },
  resources: {
    ping: {
      url: 'ping',
    },
  },
  components: {
    Dialog,
    Base,
  },
}
</script>
