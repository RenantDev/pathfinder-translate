/**
 *  
 * By: Mutar (Renant)
 * Collaborator: Xhiriu (Pedro)
 * 
 * Site: www.mutar.com.br
 * Create: 18/02/2020
 * 
 * Version 1.0.0 (20/02/2020)
 *  
 * */


// FS
var fs = require("fs");

// Parametros de Tradução
var traduzir_para = "pt";
var api_tradutor = "API_KEY_GOOGLE_TRANSLATE";
var googleTranslate = require('google-translate', null)(api_tradutor);

// Array de textos
var lista_de_textos;
var text = {
    "strings": [
        {
            "Key": "ee15f0be-712b-40ba-8d1b-6575ece633e6",
            "Value": "Damage bonus"
        },
        {
            "Key": "1a7cf3bf-cb34-488b-9469-7f92176211e5",
            "Value": "Attract critters from the whole area."
        },
        {
            "Key": "246accef-137b-4e59-bcc9-af8c83561dcc",
            "Value": "Feed Critters"
        },
    ]
};

// Define o arquivo JSON
console.log("\n *INICIO DA TRADUÇÃO* \n");

// Leitura de arquivo
function leituraArquivo() {
    return new Promise((resolve, reject) => {
        var contents = fs.readFileSync("enGB.json");
        resolve(JSON.parse(contents));

    });

}

// Define array do arquivo
async function defineArrayTexto() {
    await leituraArquivo().then(res => {
        this.lista_de_textos = res;
        return res;
    });
}

defineArrayTexto();

// Define se o projeto esta em produção ou em desenvolvimento
var prod = true; // true or false
var variable = prod ? this.lista_de_textos : text;

// Traduzir texto
function traduzirTexto(texto, i) {

    return new Promise((resolve, reject) => {
        // if (!!texto) { resolve(texto); }
        googleTranslate.translate(texto, traduzir_para, function (err, translation) {
            if (err) { reject(err); }
            // console.log(translation.translatedText);
            try {
                resolve(translation.translatedText);
            } catch (error) {
                resolve(texto);
                // fs.rename('traduzido.json', 'traduzido_' + i + '.json', function (err) {
                //     if (err) throw err;
                //     console.log('renamed complete');
                // });

            }
        });
    });

}

var startIndex = 0;

async function translateText(i = 0) {

    if (i < variable.strings.length) {
        try {
                await traduzirTexto(variable.strings[i].Value, i).then(res => {
                    try {
                        // Aux
                        var auxVal = variable.strings[i].Value;
                        // Define o que vai ser escrito no arquivo
                        variable.strings[i].Value = res;

                        console.log(`%c ${i} OK`, 'color: #4cff00');

                        writeFile(i, prod);
                        
                        translateText(i + 1);

                    } catch{
                        process.exit();
                    }


                    if (i == variable.strings.length - 1) {
                        console.log('Tradução concluida!');
                    }
                });


        } catch (error) {
            console.log(`%c ${i} ERROR`, 'color: #4cff00');
            // variable.strings[i].Value = '';
            // writeFile(i, prod);
            setTimeout(function(){
                translateText(i);
            }, 50000);
        }
    }
}

// Escreve no arquivo JSON
function writeFile(i = 0, write) {
    if (write) {

        // Inicia o arquivo JSON
        if (i == 0) {
            fs.appendFile('traduzido.json', '{ "$id": "1", "strings": [ ', function (err) {

            });
        }

        try {
            if (i != 0) {
                // Escreve no arquivo JSON
                fs.appendFile('traduzido.json', JSON.stringify(variable.strings[i]) + ', ', function (err) {
                    if (err) {
                        console.log('error to add line');
                    } else {
                        console.log(`%c Write: ${i} OK`, 'color: #4cff00');
                    }
                });
            }
        } catch (error) {
            console.log(`%c ${i} Write: FAIL`, 'color: #4cff00');
        }

        // Finaliza o arquivo JSON
        if (i == variable.strings.length - 1) {
            fs.appendFile('traduzido.json', '] }', function (err) {
                if (err) {
                    console.log('error to end line');
                } else {
                    console.log(`%c Write: End OK`, 'color: #4cff00');
                }
            });
        }
    } else {
        // Imprime na tela o que vai ser escrito no JSON
        console.log('fake write', JSON.stringify(variable.strings[i].Value, 2, undefined));
    }
};

setTimeout(function startScript(i = 0) {
    if (this.lista_de_textos) {
        variable = this.lista_de_textos;
        //    console.log(lista_de_textos);
        translateText(startIndex);
    } else {
        console.log('verificado ' + i);
        setTimeout(function () {
            startScript(i + 1);
        }, 1000);
    }
}, 1000);





