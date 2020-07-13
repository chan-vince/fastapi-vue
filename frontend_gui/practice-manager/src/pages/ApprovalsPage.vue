<template>
  <div>
    <NavBar ref="navBar" />
    <div class="container" style="max-width: 1920px">
      <div class="card" id="spacing-margins-card">
        <div class="card-content">
          <b-tabs id="spacing-margins-tabs">
            <b-tab-item label="Pending">
                <PendingApprovalsTable
                  id="tables"
                  ref="pendingEmployeeApprovals"
                  v-bind:pendingOnly="true"
                  @refresh="refreshTables"
                  style="margin: 0px 20px 120px 20px"
                />
            </b-tab-item>
            <b-tab-item label="History">
                <!-- <PracticeApprovalsTable
                  id="tables"
                  ref="pendingPracticeApprovals"
                  v-bind:pendingOnly="true"
                  @refresh="refreshTables"
                  style="margin: 0px 20px 120px 20px"
                /> -->
            </b-tab-item>
          </b-tabs>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "../components/NavBar";
import PendingApprovalsTable from "../components/PendingApprovalsTable";

export default {
  name: "ApprovalsPage",
  components: {
    NavBar,
    PendingApprovalsTable
  },
  // data() {
  // },
  created() {
    console.log("Approvals Page");
  },
  methods: {
    refreshTables() {
      console.log("Time to refresh!");
      // this.$refs.pendingPracticeApprovals.getStagingPractices();
      // this.$refs.historicPracticeApprovals.getStagingPractices();
      // this.$refs.pendingEmployeeApprovals.getStagingEmployees();
      // this.$refs.historicEmployeeApprovals.getStagingEmployees();
      // this.$refs.navBar.getPendingApprovalsCount();
    }
  }
};
</script>

<style scoped>
#spacing-margins-card {
  margin: 10px 25px 25px 25px;
}
#spacing-margins-tabs {
  margin: 0px 20px 40px 20px;
}
#tables{  
  min-height: 600px;
}
</style>