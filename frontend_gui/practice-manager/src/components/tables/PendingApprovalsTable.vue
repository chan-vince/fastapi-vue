<template>
    <section>
        <b-table
                ref="table"
                paginated
                per-page="20"
                :loading="loading"
                :data="staging_records"
                :show-detail-icon="showDetailIcon"
                :opened-detailed="defaultOpenedDetails"
                :detailed="pendingOnly"
                @details-open="getSupportInfo"
                detail-key="id"
                aria-next-label="Next page"
                aria-previous-label="Previous page"
                aria-page-label="Page"
                aria-current-label="Current page"
        >
            <template slot-scope="props">
                <b-table-column field="id" label="Request Type" sortable>
                    <template v-if="props.row.target_id == null">Add New&nbsp;</template>
                    <template v-else>Modify&nbsp;</template>
                    <template>{{ target_tables[props.row.target_table] }}</template>
                </b-table-column>

                <b-table-column field="last_modified" label="Request Date" sortable>
                    <span class>{{ new Date(props.row.last_modified).toLocaleString() }}</span>
                </b-table-column>

                <b-table-column field="requestor.name" label="Requested By" sortable>
                    <template v-if="pendingOnly"></template>
                    {{ props.row.requestor.name }}
                </b-table-column>

                <b-table-column field="approved" label="Status" sortable>
                    <template v-if="props.row.approved == 1">
                        <b-tag type="is-success" rounded>Approved</b-tag>
                    </template>
                    <template v-else-if="props.row.approved == 0">
                        <b-tag type="is-danger" rounded>Rejected</b-tag>
                    </template>
                    <template v-else>
                        <b-tag rounded>Pending</b-tag>
                    </template>
                </b-table-column>
            </template>

            <template slot="detail" slot-scope="props">
                <template v-if="props.row.target_table === 'ip_ranges'">
                    <PendingIPRangeDetail
                            v-bind:row="props.row"
                            v-bind:aux_info="aux_info"
                            v-bind:detail_delta="detail_delta"/>
                </template>

                <template v-if="props.row.target_table === 'practices'">
                    <PendingPracticeDetail
                            v-bind:row="props.row"
                            v-bind:aux_info="aux_info"
                            v-bind:detail_delta="detail_delta"/>
                </template>
                <template v-if="props.row.target_table === '_association_practice_systems'">
                    <PendingAccessSystemDetail
                            v-bind:row="props.row"
                            v-bind:aux_info="aux_info"
                            v-bind:detail_delta="detail_delta"/>
                </template>
                <template v-if="props.row.target_table === 'employees'">
                    <PendingEmployeeDetail
                            v-bind:row="props.row"
                            v-bind:aux_info="aux_info"
                            v-bind:detail_delta="detail_delta"/>
                </template>
                <!-- <template v-if="props.row.target_id == null">
                  {{ props.row.payload }}
                  {{ aux_info }}
                </template>
                <template v-else>
                  <div v-for="item in detail_delta" :key="item.key">{{item}}</div>
                </template>-->

                <!-- <template v-if="props.row.source_id == null">
                  <div v-for="item in diff_data" :key="item.name">
                    <div class="level-left">
                      {{  }}
                      <div class="level-item">
                        <strong>{{ item.label }}:</strong>
                      </div>
                      <div class="level-item">{{props.row[item.field]}}</div>
                    </div>
                  </div>
                </template>-->

                <!-- <template v-else>
                  <div class="title is-5">Changes:</div>
                  <div v-for="item in staging_records" :key="item.name">
                    <template v-if="props.row.source[item.field] != props.row[item.field]">
                      <div class="columns">
                        <div class="column is-2">
                          <strong>{{ item.label }}:</strong>
                        </div>
                        <div class="column">
                          <div class="level">
                            <div class="level-left">
                              <b-tag size="is-medium" type="is-danger">{{props.row.source[item.field]}}</b-tag>
                              <b-icon icon="arrow-right"></b-icon>
                              <b-tag size="is-medium" type="is-success">{{props.row[item.field]}}</b-tag>
                            </div>
                          </div>
                        </div>
                      </div>
                    </template>
                  </div>
                </template>-->
                <template v-if="pendingOnly">
                    <hr/>
                    <div class="buttons">
                        <b-button
                                type="is-success"
                                outlined
                                icon-left="check"
                                v-on:click="acceptChanges(props.row['id'])"
                        >Accept
                        </b-button>
                        <b-button
                                type="is-danger"
                                outlined
                                icon-left="close"
                                v-on:click="rejectChanges(props.row['id'])"
                        >Reject
                        </b-button>
                    </div>
                </template>
            </template>

            <template slot="empty">
                <section class="section">
                    <div class="content has-text-grey has-text-centered">
                        <p>
                            <b-icon
                                    icon="emoticon-happy"
                                    size="is-large">
                            </b-icon>
                        </p>
                        <p>No pending approvals!</p>
                    </div>
                </section>
            </template>
        </b-table>
    </section>
</template>


<script>
    import {client} from "../../api.js";
    import PendingIPRangeDetail from "../approval_details/PendingIPRangeDetail.vue";
    import PendingPracticeDetail from "../approval_details/PendingPracticeDetail";
    import PendingAccessSystemDetail from "../approval_details/PendingAccessSystemDetail";
    import PendingEmployeeDetail from "../approval_details/PendingEmployeeDetail";

    export default {
        name: "PendingApprovalsTable",
        props: ["pendingOnly"],
        components: {
            PendingEmployeeDetail,
            PendingIPRangeDetail,
            PendingPracticeDetail,
            PendingAccessSystemDetail
        },
        data() {
            return {
                staging_records: [],
                detail_delta: {},
                defaultOpenedDetails: [],
                showDetailIcon: true,
                loading: true,
                target_tables: {
                    ip_ranges: "CIDR IP Range",
                    practices: "Practice",
                    employees: "Employee",
                    _association_practice_systems: "System Access"},
                aux_info: null,
                details_close: null
            };
        },
        methods: {
            getStagingPractices(skip, limit) {
                client
                    .get(`api/v1/stagingbeta`, {
                        params: {skip: skip, limit: limit}
                    })
                    .then(response => {
                        this.staging_records = response.data.filter(
                            item => item.approved == null
                        );
                        this.loading = false;
                    });
            },
            getSupportInfo(row) {
                client
                    .get(`api/v1/stagingbeta/delta`, {
                        params: {id: row.id}
                    })
                    .then(response => {
                        this.detail_delta = response.data.deltas;
                        this.defaultOpenedDetails = [row.id];
                    })
                    .catch(error => {
                        console.log(error);
                    });

                // Get the referenced address for an ip_range
                if (row.target_table === "ip_ranges") {
                    client
                        .get(`api/v1/practice/address_id`, {
                            params: {address_id: row.payload.address_id}
                        })
                        .then(response => {
                            this.aux_info = response.data;
                        })
                        .catch(error => {
                            console.log(error);
                        });
                }
                // modify existing practice
                else if (row.target_table === "practices" && row.target_id !== null) {
                    client
                        .get(`api/v1/practice/id`, {
                            params: {practice_id: row.target_id}
                        })
                        .then(response => {
                            this.aux_info = response.data;
                        })
                        .catch(error => {
                            console.log(error);
                        });
                }
                // add new practice
                else if (row.target_table === "practices" && row.target_id === null) {
                    this.aux_info = {}
                }
                // access systems
                else if (row.target_table === "_association_practice_systems") {
                    client
                        .get(`api/v1/practice/id`, {
                            params: {practice_id: row.target_id}
                        })
                        .then(response => {
                            this.aux_info = response.data;
                        })
                        .catch(error => {
                            console.log(error);
                        });
                }
                // modify existing employee
                else if (row.target_table === "employees" && row.target_id !== null){
                    client
                        .get(`api/v1/employee/id`, {
                            params: {employee_id: row.target_id}
                        })
                        .then(response => {
                            this.aux_info = response.data;
                        })
                        .catch(error => {
                            console.log(error);
                        });
                }
                // add new employee
                else if (row.target_table === "employees" && row.target_id === null) {
                    this.aux_info = {}
                }
            },
            acceptChanges(id) {
                var current = this;
                console.log(`Accepting changes for row id ${id}`);
                client
                    .put(`api/v1/stagingbeta/approve`, null, {
                        params: {staging_id: id, approver_id: 5000}
                    })
                    .then(response => {
                        console.log(response.data);
                        this.$buefy.toast.open({
                            message: "Accepted change successfully",
                            type: "is-success"
                        });
                        this.$emit("refresh");
                    })
                    .catch(function (error) {
                        console.log(error);
                        current.$buefy.toast.open({
                            message: "Could not accept change",
                            type: "is-danger"
                        });
                    });
            },
            rejectChanges(id) {
                var current = this;
                console.log(`Rejecting changes for row id ${id}`);
                client
                    .put(`api/v1/stagingbeta/reject`, null, {
                        params: {staging_id: id, approver_id: 5000}
                    })
                    .then(response => {
                        console.log(response.data);
                        this.$buefy.toast.open({
                            message: "Rejected change successfully",
                            type: "is-success"
                        });
                        this.$emit("refresh");
                    })
                    .catch(function (error) {
                        console.log(error);
                        current.$buefy.toast.open({
                            message: "Could not reject change",
                            type: "is-danger"
                        });
                    });
            },
            goToPractice(rowObject) {
                this.$router.push({path: `/practice/${rowObject["name"]}`});
            }
        },
        created() {
            this.loading = true;
            this.getStagingPractices();
        }
    };
</script>


<style scoped>
</style>