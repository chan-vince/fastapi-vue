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
                :loading="loading"
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
                <template v-for="column in columns">
                    <b-table-column :key="column.id" v-bind="column">
                        <template
                            v-if="column.searchable"
                            slot="searchable"
                            slot-scope="props">
                            <b-input
                                v-model="props.filters[props.column.field]"
                                placeholder="Search..."
                                icon="magnify"
                                size="is-small" />
                        </template>
                        <template
                            v-if="!('list_target' in column)">
                            {{ props.row[column.field] }}
                        </template>
                        <template
                            v-else>
                            {{ props.row[column.field].map(a => a[column.list_target]).join(", ") }}
                        </template>
                    </b-table-column>
                </template>
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
                columns: [{field: 'id',label: 'ID', width: '100', numeric: true},
                          {field: 'created_date', label: 'Date Created', searchable: true,},
                          {field: 'name', label: 'Practice Name', searchable: true,},
                          {field: 'national_code', label: 'National Code', searchable: true,},
                          {field: 'emis_cdb_practice_code', label: 'EMIS CDB Practice Code', searchable: true,},
                          {field: 'access_systems', label: 'Access System(s)', list_target: 'name',},
                          {field: 'ip_ranges', label: 'IP Range(s)', list_target: 'cidr',},
                          {field: 'phone_num', label: 'Phone Number', searchable: true,}],
                loading: false,
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
            this.loading = true  
            client.get(`api/v1/practice/`, {params: { skip: 0, limit: 1000 }})
            .then(response => {
                this.data = response.data
                this.loading = false
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