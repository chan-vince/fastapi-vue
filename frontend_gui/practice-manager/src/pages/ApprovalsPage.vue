<template>
    <div>
        <NavBar ref="navBar"/>
        <div class="container" style="max-width: 1920px">
            <div class="card" id="spacing-margins-card">
                <div class="card-content">
                    <b-tabs id="spacing-margins-tabs">
                        <b-tab-item label="Pending">
                            <PendingApprovalsTable
                                    id="tablesPending"
                                    ref="pendingApprovalsTable"
                                    v-bind:pendingOnly="true"
                                    @refresh="refreshTables"
                            />
                        </b-tab-item>
                        <b-tab-item label="History">
                            <PendingApprovalsTable
                                    id="tablesHistory"
                                    ref="historyApprovalsTable"
                                    v-bind:pendingOnly="false"
                                    @refresh="refreshTables"
                            />
                        </b-tab-item>
                    </b-tabs>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import NavBar from "../components/general/NavBar";
    import PendingApprovalsTable from "../components/tables/PendingApprovalsTable";
    // import HistoryApprovalsTable from "../components/tables/HistoryApprovalsTable";

    export default {
        name: "ApprovalsPage",
        components: {
            NavBar,
            PendingApprovalsTable,
            // HistoryApprovalsTable
        },
        // data() {
        // },
        created() {
            console.log("Approvals Page");
        },
        methods: {
            refreshTables() {
                console.log("Time to refresh!");
                this.$refs.navBar.getPendingApprovalsCount()
                this.$refs.pendingApprovalsTable.refreshRows();
                this.$refs.historyApprovalsTable.refreshRows();
                // this.$refs.historyApprovalsTable.getStagingPractices();
            }
        }
    };
</script>

<style scoped>
    #spacing-margins-card {
        margin: 10px 25px 25px 25px;
    }

    #spacing-margins-tabs {
        margin: 0 20px 40px 20px;
    }

    #tablesPending, #tablesHistory {
        min-height: 480px;
        margin: 0 20px 120px 20px;
    }
</style>