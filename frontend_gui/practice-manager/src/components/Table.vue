<template>
    <div class="table-div">
        <section>
            <b-field grouped group-multiline>
                <b-select v-model="perPage" :disabled="!isPaginated">
                    <option value="5">5 per page</option>
                    <option value="10">10 per page</option>
                    <option value="15">15 per page</option>
                    <option value="20">20 per page</option>
                </b-select>
            </b-field>

            <b-table
                :data="data"
                :paginated="isPaginated"
                :per-page="perPage"
                :current-page.sync="currentPage"
                :pagination-simple="isPaginationSimple"
                :pagination-position="paginationPosition"
                :default-sort-direction="defaultSortDirection"
                :sort-icon="sortIcon"
                :sort-icon-size="sortIconSize"
                default-sort="name"
                aria-next-label="Next page"
                aria-previous-label="Previous page"
                aria-page-label="Page"
                aria-current-label="Current page">

                <template slot-scope="props">
                    <b-table-column field="id" label="ID" width="40" sortable numeric>
                        {{ props.row.id }}
                    </b-table-column>

                    <b-table-column field="created_date" label="Date Created" sortable>
                        {{ displayDate(props.row.created_date) }}
                    </b-table-column>

                    <b-table-column field="name" label="Practice Name" sortable>
                        {{ props.row.name }}
                    </b-table-column>

                    <b-table-column field="national_code" label="National Code" sortable>
                        {{ props.row.national_code }}
                    </b-table-column>

                    <b-table-column field="emis_cdb_practice_code" label="EMIS CDB Practice Code" sortable>
                        {{ props.row.emis_cdb_practice_code }}
                    </b-table-column>

                     <b-table-column field="access_systems" label="Access Systems">
                        {{props.row.access_systems.map(a => a.name).join(", ")}}
                    </b-table-column>

                    <b-table-column field="ip_ranges" label="IP Ranges">
                        {{props.row.ip_ranges.map(a => a.cidr).join(", ")}}
                    </b-table-column>

                    <b-table-column field="phone_num" label="Phone Number">
                        {{ props.row.phone_num }}
                    </b-table-column>

                </template>
            </b-table>
        </section>
    </div>
</template>

<script>
    import {client} from '../api.js'
    import moment from 'moment'

    export default {
        data() {
            return {
                data: [],
                isPaginated: true,
                isPaginationSimple: false,
                paginationPosition: 'bottom',
                defaultSortDirection: 'asc',
                sortIcon: 'chevron-up',
                sortIconSize: 'is-small',
                currentPage: 1,
                perPage: 20
            }
        },
        created () {    
            client.get(`api/v1/practice/`, {params: { skip: 0, limit: 50 }})
            .then(response => {
                this.data = response.data
            })
        },
        methods: {
            displayDate (datestring) {
                return moment(datestring).format("Do MMM YYYY")
            }
        }
    }
</script>


<style scoped>
    .table-div {
        padding-left: 30px;
        padding-right: 30px;
    }
</style>