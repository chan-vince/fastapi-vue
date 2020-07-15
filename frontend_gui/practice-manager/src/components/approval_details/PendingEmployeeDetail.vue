<template>
    <section v-if="aux_info">
        <b-loading :is-full-page="false" :active.sync="loading" :can-cancel="false"></b-loading>

        <div class="title is-4" v-if="row.target_id != null">
            {{ aux_info.name }}
        </div>

        <hr>
        <div v-for="(value, key) in detail_delta" :key="key">
            <div class="columns">
                <div class="column is-2">
                    <strong>{{ labels.find(x => x.key === key).label }}:</strong>
                </div>
                <div class="column">
                    <div class="level-left">
                        <template v-if="value.before">
                            <b-tag size="is-medium" type="is-danger">
                                {{ value.before }}
                            </b-tag>
                            <b-icon icon="arrow-right"></b-icon>
                        </template>
                        <b-tag size="is-medium" type="is-success">
                            {{ value.after }}
                        </b-tag>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
    import {client} from "../../api";

    export default {
        name: "PendingEmployeeDetail.vue",
        props: ["row", "aux_info", "detail_delta"],

        data() {
            return {
                loading: false,
                job_titles: [],
                labels: [
                    {key: "name", label: "Name"},
                    {key: "email", label: "Email"},
                    {key: "professional_num", label: "Professional ID"},
                    {key: "desktop_num", label: "Desktop ID"},
                    {key: "it_portal_num", label: "IT Portal ID"},
                    {key: "active", label: "Active"},
                    {key: "job_title_id", label: "Job Title ID"}
                ],
            }
        },
        watch: {
            detail_delta(n, o) {
                console.log(n, o) // n is the new value, o is the old value.
            }
        },
        methods: {
            getJobTitles() {
                client.get(`api/v1/job_titles`).then(response => {
                    this.job_titles = response.data;
                });
            }
        }
    }
</script>

<style scoped>

</style>