<template>
    <section>
        <b-table
            :data="data"
            :loading="loading"
            ref="table"
            paginated
            per-page="15"
            detailed
            detail-key="source_id"
            :show-detail-icon="showDetailIcon"
            aria-next-label="Next page"
            aria-previous-label="Previous page"
            aria-page-label="Page"
            aria-current-label="Current page">

            <template slot-scope="props">
                <b-table-column field="last_modified" label="Date" sortable centered>
                    <span class="">
                        {{ new Date(props.row.last_modified).toLocaleDateString() }}
                    </span>
                </b-table-column>

                <b-table-column field="requestor.first_name" label="Requestor" sortable>
                    <template>
                        {{ `${props.row.requestor.first_name} ${props.row.requestor.last_name}` }}
                    </template>
                </b-table-column>

                <b-table-column field="source.name" label="Practice" sortable>
                    <template>
                        {{ props.row.source.name }}
                    </template>
                </b-table-column>

                <b-table-column field="source.main_partners" label="Main Partner" sortable>
                    <template>
                        {{ props.row.source.main_partners[0].first_name }}
                        {{ props.row.source.main_partners[0].last_name }}
                    </template>
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

                <b-table-column field="approver.first_name" label="Approver" sortable>
                    <template v-if="props.row.approver">
                        {{ `${props.row.approver.first_name} ${props.row.approver.last_name}` }}
                    </template>
                </b-table-column>


            </template>

            <template slot="detail" slot-scope="props">
                <div class="title is-5">
                    Change(s):
                </div>
                <div v-for="item in diff_data" :key="item.name">
                    <template v-if="props.row.source[item.field] != props.row[item.field]">
                        <div class="columns" style="max-width: 800px">
                            <div class="column is-2">
                                <strong>{{ item.label }}:</strong>
                            </div>
                            <div class="column">
                                <b-tag size="is-medium" type="is-danger">{{props.row.source[item.field]}}</b-tag>
                            </div>
                            <div class="column is-1">
                                <b-icon icon="arrow-right"></b-icon>
                            </div>
                            <div class="column">
                                <b-tag size="is-medium" type="is-success">{{props.row[item.field]}}</b-tag>
                            </div>
                        </div>
                    </template>
                </div>
            </template>
        </b-table>
    </section>
</template>


<script>
    // const data = require('@/data/sample.json')
    import {client} from '../api.js'


    export default {
        name: 'PracticeApprovalsTable',
        props: ["pendingOnly"],
        data() {
            return {
                data: [],
                defaultOpenedDetails: [1],
                showDetailIcon: true,
                loading: true,
                diff_data: [
                    {'field': 'name','label': 'Name'},
                    {'field': 'national_code Code', 'label': 'National Code'},
                    {'field': 'emis_cdb_practice_code', 'label': 'EMIS CDB Practice Code'},
                    {'field': 'go_live_date', 'label': 'Go Live Date'},
                    {'field': 'closed', 'label': 'Closed'}]
            }
        },
        methods: {
            getStagingPractices(skip, limit) {
                client.get(`api/v1/staging/practice/`, {params: { skip: skip, limit: limit }})
                .then(response => {
                    if(this.$props.pendingOnly){
                        this.data = response.data.filter(item => item.approved == null)    
                    }
                    else{
                        this.data = response.data.filter(item => item.approved != null)
                    }
                    this.loading = false
                    // this.$buefy.toast.open(`Expanded`)
                })
            }
        },
        created () { 
            this.loading = true
            this.getStagingPractices()
        }
    }
</script>



<style scoped>

</style>