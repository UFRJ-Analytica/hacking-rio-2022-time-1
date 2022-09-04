<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on, attrs }">
      <v-card>
        <v-card-title>
          Tartarugas Encontradas
          <v-spacer></v-spacer>

          <v-btn
            v-if="filter"
            :disabled="!filter"
            class="white--text"
            color="red"
            @click="closeFilter"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-btn
            v-else
            :disabled="filter"
            class="white--text"
            color="grey darken-2"
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-filter-variant</v-icon>
          </v-btn>
        </v-card-title>
        <v-data-table
          disable-sort
          hide-default-footer
          :headers="headers"
          :items="items"
          :page.sync="page"
          :items-per-page="itemsPerPage"
        >
          <template v-slot:[`item.nome`]="{ item }">
            <NuxtLink
              :to="{
                path: `/turtle/${item.nome.toLowerCase()}`,
              }"
            >
              {{ item.nome }}
            </NuxtLink>
          </template>

          <template v-slot:[`item.local`]="{ item }">
            {{ item.cidade }}
          </template>
        </v-data-table>
        <v-pagination
          v-model="page"
          :total-visible="7"
          color="orange darken-3"
          :length="pageCount"
          circle
          @next="readTableData"
          @previous="readTableData"
          @input="readTableData"
        ></v-pagination>
      </v-card>
    </template>

    <v-card>
      <v-card-title>
        <span class="text-h5">Filtros</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row class="select">
            <v-autocomplete
              v-model="nome"
              :items="nomes"
              color="orange darken-3"
              label="Nome da Tartaruga"
              @change="onSelectedName"
            ></v-autocomplete>
          </v-row>
          <v-row>
            <v-autocomplete
              v-model="estado"
              label="Estado"
              outlined
              single
              color="orange darken-3"
              background-color="#F2F2F2"
              :items="estados"
              @change="onSelectState"
            >
            </v-autocomplete>
          </v-row>
          <v-row>
            <v-autocomplete
              v-model="municipio"
              outlined
              single
              color="orange darken-3"
              background-color="#F2F2F2"
              :disabled="!show_municipios"
              :items="municipios"
              label="Município"
              @change="onSelectMun"
            >
            </v-autocomplete>
          </v-row>
          <v-row class="select">
            <dateDialog
              :key="dateKey"
              :range="true"
              initial-date=""
              text="Intervalo de datas"
              @onSelectedDate="
                (value) => {
                  this.date = value;
                }
              "
            ></dateDialog>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="dialog = false"> Close </v-btn>
        <v-btn text @click="save"> Save </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  data() {
    return {
      //Seleção do Estado
      estados: [],
      estado: "",
      municipios: [],
      municipio: "",
      identificadores_ufs: [],
      identificadores_mun: [],
      indicadorUF: 0,
      indicadorMUN: 0,
      show_municipios: false,

      page: 1,
      filter: false,
      pageCount: 3,
      itemsPerPage: 5,
      dialog: false,
      status: null,
      dateKey: 0,
      date: "",
      nome: "",
      menu: false,
      nomes: [],
      pags: {},
      headers: [
        { text: "Nome", value: "nome", align: "center" },
        { text: "Cidade", value: "cidade", align: "center" },
        { text: "Estado", value: "estado", align: "center" },

        { text: "Data do encontro", value: "data", align: "center" },
      ],
      items: [
        {
          id: "1",
          nome: "Rafael",
          cidade: "Rio de Janeiro",
          estado: "Rio de Janeiro",
          data: "11/11/2011"
        },
        {
          id: "2",
          nome: "Ana",
          cidade: "Santa Catarina",

          estado: "Rio de Janeiro",
          data: "11/11/2011"
        },
      ],
    };
  },
  async mounted() {
  
    const ufs = await this.$axios.$get(
      "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    );

    this.estados = ufs.map((estado) => {
      return estado.nome;
    });
    this.identificadores_ufs = ufs.map((estado) => {
      return estado.id;
    });
    const response1 = await this.$axios.$get("/samples-names");
    this.nomes = response1.nomes;

    // const response2 = await this.$axios.$get(
    //   `/samples?limit=${this.itemsPerPage}&offset=0`
    // );
    // this.pageCount = Math.ceil(response2.Count / this.itemsPerPage);
    // this.items = response2.Samples.map((item) => {
    //   const date = new Date(item.photo_date.slice(0, -4));
    //   const formattedDate = `${date.getDate()}/${
    //     date.getMonth() + 1
    //   }/${date.getFullYear()}`;
    //   return {
    //     id: item.id,
    //     v: item.vector,
    //     p: item.pathogen,
    //     data: formattedDate,
    //     status: this.legenda[item.status - 1],
    //   };
    // });
  },
  methods: {

    async onSelectState() {
      this.show_municipios = true;
      const index = this.estados.indexOf(this.estado);
      const uf = this.identificadores_ufs[index];
      const url = `https://servicodados.ibge.gov.br/api/v1/localidades/estados/${uf}/municipios`;
      const municipios = await this.$axios.$get(url);
      this.indicadorUF = uf;
      this.municipios = municipios.map((municipio) => {
        return municipio.nome;
      });
      this.identificadores_mun = municipios.map((municipio) => {
        return municipio.id;
      });
    },
    onSelectMun() {
      const index = this.municipios.indexOf(this.municipioTrabalho);
      const mun = this.identificadores_mun[index];
      this.indicadorMUN = mun;
    },
    async readTableData() {
      // const response = await this.$axios.$get(
      //   `/samples?limit=${this.itemsPerPage}&offset=${
      //     (this.page - 1) * this.itemsPerPage
      //   }`
      // );
      // this.items = response.Samples.map((item) => {
      //   const date = new Date(item.photo_date.slice(0, -4));
      //   const formattedDate = `${date.getDate()}/${
      //     date.getMonth() + 1
      //   }/${date.getFullYear()}`;
      //   return {
      //     id: item.id,
      //     v: item.vector,
      //     p: item.pathogen,
      //     data: formattedDate,
      //     status: this.legenda[item.status - 1],
      //   };
      // });
      // this.pageCount = Math.ceil(response.Count / this.itemsPerPage);
    },
    allowedDates(val) {
      // const listVal = val.split("-");
      // const StringVal = `${listVal[2]}/${listVal[1]}/${listVal[0]}`;
      // return this.databaseItems.map((item) => item.data).includes(StringVal);
    },
    onSelectedName() {
      // this.date = "";
      // this.dateKey += 1;
    },
    closeFilter() {
      // this.filter = false
      // this.ID = "";
      // this.date = "";
      // this.status = null;
      // this.dateKey += 1;
      // this.itemsPerPage = 5
      // this.readTableData();
    },
    async save() {
      // this.filter = true
      // if (this.ID) {
      //   const response = await this.$axios.$get(`/samples-info?id=${this.ID}`);
      //   const date = new Date(response.photo_date.slice(0, -4));
      //   const formattedDate = `${date.getDate()}/${
      //     date.getMonth() + 1
      //   }/${date.getFullYear()}`;
      //   this.items = [
      //     {
      //       id: this.ID,
      //       v: response.vector,
      //       p: response.pathogen,
      //       data: formattedDate,
      //       status: this.legenda[response.status - 1],
      //     },
      //   ];
      // }
      // if (this.status || this.date) {
      //   const statusKey =  this.status ?  this.legenda.indexOf(this.status) + 1 : 0
      //   const response = await this.$axios.$post(
      //     `/filter-samples`,
      //     {
      //       "status": statusKey,
      //       "date_range": this.date
      //     }
      //   );
      //   this.items = response.Samples.map((item) => {
      //     const date = new Date(item.photo_date.slice(0, -4));
      //     const formattedDate = `${date.getDate()}/${
      //       date.getMonth() + 1
      //     }/${date.getFullYear()}`;
      //     return {
      //       id: item.id,
      //       v: item.vector,
      //       p: item.pathogen,
      //       data: formattedDate,
      //       status: this.legenda[item.status - 1],
      //     };
      //   });
      //   this.itemsPerPage = this.items.length
      // }
      // this.pageCount = 1;
      // this.dialog = false;
    },
  },
};
</script>
