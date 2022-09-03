<template>
    <v-dialog
      ref="dialog"
      v-model="modal"
      :return-value.sync="date"
      persistent
      width="290px"
      color="orange darken-3"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-text-field
          v-model="date"
          :disabled="disabled"
          :label="text"
          prepend-icon="mdi-calendar"
          readonly
          color="orange darken-3"
          v-bind="attrs"
          v-on="on"
        ></v-text-field>
      </template>
      <v-date-picker
        v-model="date"
        :range="range"
        locale="pt-BR"
        scrollable
        :max="
          new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
            .toISOString()
            .substr(0, 10)
        "
        min="1950-01-01"
        color="orange darken-3"
      >
        <v-spacer></v-spacer>
        <v-btn text color="primary" @click="saveDate"> Save </v-btn>
      </v-date-picker>
    </v-dialog>
  </template>
  
  
  <script>
  export default {
    props: {
      disabled: {
        type: Boolean,
        default: false,
      },
      range: {
        type: Boolean,
        default: false,
      },
      initialDate: {
        type: String,
        default: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
          .toISOString()
          .substr(0, 10),
      },
      text: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        modal: false,
        date: this.initialDate,
      };
    },
    methods: {
      saveDate() {
        this.modal = false;
        this.$refs.dialog.save(this.date);
        this.$emit("onSelectedDate", this.date);
      },
    },
  };
  </script>
  