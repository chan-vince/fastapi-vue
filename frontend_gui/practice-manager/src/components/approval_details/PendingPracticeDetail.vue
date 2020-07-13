<template>
    <section v-if="aux_info">
        <b-loading :is-full-page="false" :active.sync="loading" :can-cancel="false"></b-loading>

        <strong v-if="Object.keys(aux_info).length !== 0">{{ aux_info.name }}
            <hr>
        </strong>
        <div v-for="(element, index) in elements" :key="index">
            <template v-if="(aux_info[element.key] != row.payload[element.key]) && (row.payload[element.key])">
                <div class="columns">
                    <div class="column is-2">
                        <strong>{{ element.label }}</strong>
                    </div>
                    <div class="column">
                        <div class="level-left">
                            <template v-if="row.modify">
                                <template v-if="element.label === 'Access Systems'">
                                    <b-tag size="is-medium" type="is-success">{{ row.payload[element.key].join(" and ") }}</b-tag>
                                </template>
                                <template v-else>
                                    <b-tag size="is-medium" type="is-danger">{{ aux_info[element.key] }}</b-tag>
                                    <b-icon icon="arrow-right"></b-icon>
                                    <b-tag size="is-medium" type="is-success">{{ row.payload[element.key] }}</b-tag>
                                </template>
                            </template>
                            <template v-else>
                                <template v-if="element.label === 'Closed'">
                                    {{ row.payload[element.key] ? "Yes" : "No" }}
                                </template>
                                <template v-else>
                                    {{ row.payload[element.key] }}
                                </template>
                            </template>
                        </div>
                    </div>
                </div>
            </template>
        </div>
    </section>
</template>

<script>
    export default {
        name: "PendingPracticeDetail.vue",
        props: ["row", "aux_info", "detail_delta"],
        data() {
            return {
                loading: false,
                elements: [
                    {"label": "Practice Name", "key": "name"},
                    {"label": "National Code", "key": "national_code"},
                    {"label": "EMIS CDB Practice Code", "key": "emis_cdb_practice_code"},
                    {"label": "Go Live Date", "key": "go_live_date"},
                    {"label": "Closed", "key": "closed"},
                    {"label": "Access Systems", "key": "access_systems"}
                ],
            }
        }
    }
</script>

<style scoped>

</style>