<template>
    <section v-if="aux_info">
        <b-loading :is-full-page="false" :active.sync="loading" :can-cancel="false"></b-loading>

        <div class="title is-4" v-if="row.target_id != null">
            {{ aux_info.name }}
        </div>

        <hr>
        <div v-for="label in labels" :key="label.key">
            <template v-if="detail_delta[label.key].before !== detail_delta[label.key].after">
                <div class="columns">
                    <div class="column is-2">
                        <strong>{{ label.label }}:</strong>
                    </div>
                    <div class="column">
                        <div class="level">
                            <div class="level-left">
                                <b-tag size="is-medium" type="is-danger">{{detail_delta[label.key].before}}</b-tag>
                                <b-icon icon="arrow-right"></b-icon>
                                <b-tag size="is-medium" type="is-success">{{detail_delta[label.key].after}}</b-tag>
                            </div>
                        </div>
                    </div>
                </div>
            </template>
        </div>
    </section>
</template>

<script>
    export default {
        name: "PendingEmployeeDetail.vue",
        props: ["row", "aux_info", "detail_delta"],

        data() {
            return {
                loading: true,
                labels: [{key: "name", label: "Name"}]
            }
        },
        watch: {
            aux_info() {
                if (this.aux_info !== null) {
                    this.loading = false
                }
            },
        },
    }
</script>

<style scoped>

</style>