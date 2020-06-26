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
                :total="total"
                backend-pagination
                paginated
                :per-page="perPage"
                @page-change="onPageChange"
                :current-page.sync="currentPage"
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
                            slot="searchable">
                            <b-input
                                v-model="practiceSearch"
                                v-on:input="getPractice"
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
                columns: [
                    {field: 'id',label: 'ID', width: '100', numeric: true},
                    {field: 'created_date', label: 'Date Created', searchable: true,},
                    {field: 'name', label: 'Practice Name', searchable: true,},
                    {field: 'national_code', label: 'National Code', searchable: true,},
                    {field: 'emis_cdb_practice_code', label: 'EMIS CDB Practice Code', searchable: true,},
                    {field: 'access_systems', label: 'Access System(s)', list_target: 'name',},
                    {field: 'ip_ranges', label: 'IP Range(s)', list_target: 'cidr',},
                    {field: 'phone_num', label: 'Phone Number', searchable: true,}
                ],
                total: 0,
                practice_names: [],
                loading: false,
                isPaginated: true,
                isPaginationSimple: false,
                paginationPosition: 'bottom',
                defaultSortDirection: 'asc',
                sortIcon: 'chevron-up',
                sortIconSize: 'is-small',
                perPage: 15,
                currentPage: 1,
                practiceSearch: ""
            }
        },
        methods: {
            displayDate (datestring) {
                return moment(datestring).format("Do MMM YYYY")
            },
            getPractices(skip, limit) {
                client.get(`api/v1/practice/`, {params: { skip: skip, limit: limit }})
                .then(response => {
                    this.data = response.data
                    this.loading = false
                })
            },
            onPageChange(page) {
                let skip = (page * this.perPage) - this.perPage
                let limit = this.perPage
                this.currentPage = page
                if(this.practiceSearch.length == 0){
                    this.getPractices(skip, limit)
                }
            },
            getPractice(){
                if (this.practiceSearch.length > 0){
                    this.loading = true
                    var names = this.practice_names.filter(name => name.toLowerCase().includes(this.practiceSearch.toLowerCase()))
                    var practice_details = []
                    var promises = []
                    for (const name of names) {
                        promises.push(
                            client.get(`api/v1/practice/name/`, {params: {name: name} })
                            .then(response => {
                                practice_details.push(response.data)
                            })
                        )
                    }
                    Promise.all(promises).then(() => {
                        // Need to check the length again once the promise returns as its likely that the search input is deleted before the return
                        if (this.practiceSearch.length != 0){
                            this.total = practice_details.length
                        }
                        this.data = practice_details
                        this.currentPage = 1
                        this.loading = false
                    });                    
                }
                else{
                    this.getPractices(0, this.perPage)
                    this.getTotalPractices()
                }
            },
            getTotalPractices(){
                client.get(`api/v1/practice/count`)
                .then(response => {
                    this.total = response.data.count
                })
            },
            getAllPracticeNames(){
                client.get(`api/v1/practice/names`)
                .then(response => {
                    this.practice_names = response.data.names
                })
            },
        },
        created () {  
            this.loading = true
            this.getTotalPractices()
            this.getAllPracticeNames()
            this.getPractices(0, this.perPage)    
        },
    }
</script>


<style scoped>
    .table-div {
        padding-left: 30px;
        padding-right: 30px;
    }
</style>