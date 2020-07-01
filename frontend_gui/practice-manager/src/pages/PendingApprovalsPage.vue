<template>
    <div>
      <NavBar/>
      <div class=card id=spacing-margins-card>
          <div class=card-header-title>
            Pending Approvals
          </div>
          <b-tabs v-model="activeTab" id=spacing-margins-tabs>
            <b-tab-item label="Practices">
                insert practices table component
            </b-tab-item>
            <b-tab-item label="Employees">
                insert employees table
            </b-tab-item>
          </b-tabs>
      </div>
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

#spacing-margins-card {
    margin: 40px 40px 40px 40px;
}
#spacing-margins-tabs {
    margin: 40px 10px 40px 10px;
}

</style>