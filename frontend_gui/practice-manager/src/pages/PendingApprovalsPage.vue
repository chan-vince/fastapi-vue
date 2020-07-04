<template>
  <div>
    <NavBar ref="navBar" />
    <div class="container" style="max-width: 1920px">
      <div class="card" id="spacing-margins-card">
        <div class="card-content">
          <b-tabs id="spacing-margins-tabs">
            <b-tab-item label="Practices">
              <br />
              <div class="card-header-title">Pending Practice Approvals</div>
              <div class="card">
                <PracticeApprovalsTable
                  ref="pendingPracticeApprovals"
                  v-bind:pendingOnly="true"
                  @refresh="refreshTables"
                  style="margin: 0px 20px 120px 20px"
                />
              </div>

              <hr />
              <div class="card-header-title">Approval History</div>
              <div class="card">
                <PracticeApprovalsTable
                  ref="historicPracticeApprovals"
                  v-bind:pendingOnly="false"
                  @refresh="refreshTables"
                  style="margin: 0px 20px 0px 20px"
                />
              </div>
            </b-tab-item>
            <b-tab-item label="Employees">
              <br />
              <div class="card-header-title">Pending Employee Approvals</div>
              <div class="card">
                <EmployeeApprovalsTable
                  ref="pendingEmployeeApprovals"
                  v-bind:pendingOnly="true"
                  @refresh="refreshTables"
                  style="margin: 0px 20px 120px 20px"
                />
              </div>

              <hr />
              <div class="card-header-title">Approval History</div>
              <div class="card">
                <EmployeeApprovalsTable
                  ref="historicEmployeeApprovals"
                  v-bind:pendingOnly="false"
                  @refresh="refreshTables"
                  style="margin: 0px 20px 0px 20px"
                />
              </div>
            </b-tab-item>
          </b-tabs>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "../components/NavBar";
import PracticeApprovalsTable from "../components/PracticeApprovalsTable";
import EmployeeApprovalsTable from "../components/EmployeeApprovalsTable";

export default {
  name: "PendingApprovalsPage",
  components: {
    NavBar,
    PracticeApprovalsTable,
    EmployeeApprovalsTable
  },
  // data() {
  // },
  created() {
    console.log("Pending Approvals Page");
  },
  methods: {
    refreshTables() {
      console.log("Time to refresh!");
      this.$refs.pendingPracticeApprovals.getStagingPractices();
      this.$refs.historicPracticeApprovals.getStagingPractices();
      this.$refs.pendingEmployeeApprovals.getStagingEmployees();
      this.$refs.historicEmployeeApprovals.getStagingEmployees();
      this.$refs.navBar.getPendingApprovalsCount();
    }
  }
};
</script>

<style scoped>
#spacing-margins-card {
  margin: 40px 0px 40px 0px;
}
#spacing-margins-tabs {
  margin: 10px 20px 40px 20px;
}
</style>