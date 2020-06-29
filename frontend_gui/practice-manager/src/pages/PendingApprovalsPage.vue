<template>
    <div>
      <NavBar/>
  </div>
</template>

<script>

import NavBar from '../components/NavBar'

export default {
    name: "PendingApprovalsPage",
    components: {
        NavBar
    },
    created () {
        console.log("Pending Approvals Page")
    }
}
</script>

<style scoped>

</style>