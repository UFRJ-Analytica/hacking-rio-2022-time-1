<template>
    <v-container>
        
    
            <v-row>
                
                <v-img
                    max-width="250"
                    max-height="250"
    
                    :src="require('../static/turtle.png')"
                ></v-img>
                
            </v-row>
            <v-row class="text-center" style="max-width: 350px;">
        
            <p>   Todo ano milhares de tartarugas marinhas morrem com o lixo nos oceanos.</p>
            <p>Quando pensamos no nosso impacto ecológico, nem sempre lembramos delas. Para evitar isso, vamos te apresentar as tartarugas da sua região!</p>

                
            </v-row>
    
            <v-row>
           
                    <v-btn @click="$router.push('/home')">Vamos começar?</v-btn>
            </v-row>

    </v-container>
</template>

<script>
</script>

