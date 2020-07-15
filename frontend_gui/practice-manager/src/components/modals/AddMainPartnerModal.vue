<template>
    <div class="modal-card" style="margin: 0px 50px 0px 50px">
        <header class="modal-card-head">
            <p class="modal-card-title">Add Employee to Main Partners</p>
        </header>
        <section class="modal-card-body">
            <b-field label="Employee" horizontal>
                <b-select placeholder="">
                    <option
                        v-for="employee in employees.sort((a, b) => a.name.localeCompare(b.name))"
                        :value="`${employee.name}`"
                        :key="employee.id">
                        {{ `${employee.name}` }}
                    </option>
                </b-select>
            </b-field>
        </section>
        <footer class="modal-card-foot">
            <button class="button is-primary">Save</button>
            <button class="button" type="button" @click="$parent.close()">Cancel</button>
        </footer>
    </div>
</template>


<script>
    export default {
       name: 'AddMainPartnerModal',
        props: ["employees"],
        components: {
            
        },
        data() {
            return {
                isComponentModalActive: false,
            }
        },
        created () {
            // console.log(this.$props.jobTitles)
            // console.log(this.$props.rowObject)
        }
    }
</script>