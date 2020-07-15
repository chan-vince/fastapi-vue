<template>
    <section v-if="aux_info">
        <b-loading :is-full-page="false" :active.sync="loading" :can-cancel="false"></b-loading>

        <div class="title is-4" v-if="row.target_id != null">
            <router-link :to="`/practice/${aux_info.name}`">{{ aux_info.name }}</router-link>
            <hr>
        </div>

        <template>
            <div class="columns">
                <div class="column is-2">
                    <strong>Access Systems:</strong>
                </div>
                <div class="column">
                    <div class="level">
                        <div class="level-left">
                            <b-tag size="is-medium" type="is-danger">{{ this.before_systems ? this.before_systems : "None"}}</b-tag>
                            <b-icon icon="arrow-right"></b-icon>
                            <b-tag size="is-medium" type="is-success">{{ this.after_systems ? this.after_systems : "None"}}</b-tag>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </section>
</template>

<script>
    export default {
        name: "PendingAccessSystemDetail.vue",
        props: ["row", "aux_info", "detail_delta"],

        data() {
            return {
                loading: true,
                access_systems: [{"name": "ICE", "id": 1}, {"name": "SystemOne", "id": 2}, {
                    "name": "Vision 3",
                    "id": 3
                }],
                before_systems: [],
                after_systems: [],
                prefix_word: ""
            }
        },
        watch: {
            aux_info() {
                if (this.aux_info !== null) {
                    this.loading = false
                }
            },
            detail_delta() {
                this.before_systems = this.access_systems.filter(x => this.$props.detail_delta.before.includes(x.id)).map(x => x.name).join(", ")
                this.after_systems = this.access_systems.filter(x => this.$props.detail_delta.after.includes(x.id)).map(x => x.name).join(", ")
            }
        },
    }
</script>

<style scoped>

</style>