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
                :detailed="false"
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

                <b-table-column field="last_modified" label="Modified On" sortable>
                    <span class>{{ new Date(props.row.last_modified).toLocaleString() }}</span>
                </b-table-column>

                <b-table-column field="requestor.name" label="Requested By" sortable>
                    {{ props.row.requestor.name }}
                </b-table-column>

                <b-table-column field="approver.name" label="Approved By" sortable>
                    {{ props.row.approver.name }}
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
                <div v-for="(item, key) in props.row.payload" :key="key">
                    <div class="columns">
                        <strong class="column is-3"> {{ display_headings[key] }}:</strong>
                        <p class="column"> {{ item }} </p>
                    </div>
                </div>
            </template>

            <template slot="empty">
                <section class="section">
                    <div class="content has-text-grey has-text-centered">
                        <p>
                            <b-icon
                                    icon="clipboard-outline"
                                    size="is-large">
                            </b-icon>
                        </p>
                        <p>No previous approvals.</p>
                    </div>
                </section>
            </template>
        </b-table>
    </section>
</template>


<script>
    import {client} from "../../api.js";

    export default {
        name: "PendingApprovalsTable",
        props: ["pendingOnly"],
        data() {
            return {
                staging_records: [],
                detail_delta: {},
                defaultOpenedDetails: [1],
                showDetailIcon: true,
                loading: true,
                target_tables: {
                    ip_ranges: "CIDR IP Range",
                    practices: "Practice",
                    employees: "Employee",
                    _association_practice_systems: "System Access"},
                aux_info: null,
                details_close: null,
                display_headings: {
                    name: "Name",
                    national_code: "National Code",
                    emis_cdb_practice_code: "EMIS CDB Practice Code",
                    go_live_date: "Go Live Date",
                    closed: "Closed",
                    cidr: "CIDR",
                    address_id: "Address ID#"
                },
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
                            item => item.approved !== null
                        );
                        this.loading = false;
                        console.log(this.staging_records)
                    })
                    .catch(error => {
                        console.log(error)
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
                else if (row.target_table === "practices" && row.modify === true) {
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