const reemplazos = [
    {
        char: '{',
        reemplazo: 'abre llave'
    },
    {
        char: '}',
        reemplazo: 'cierra llave'
    },
    {
        char: '(',
        reemplazo: 'abre paréntesis'
    },
    {
        char: ')',
        reemplazo: 'cierra paréntesis'
    },
    {
        char: ';',
        reemplazo: 'puntoycoma'
    },
    {
        char: '.',
        reemplazo: 'punto'
    },
    {
        char: '"',
        reemplazo: 'comilla doble'
    },
    {
        char: "'",
        reemplazo: 'comilla simple'
    },
    {
        char: '[',
        reemplazo: 'abre corchete'
    },
    {
        char: ']',
        reemplazo: 'cierra corchete'
    },
    {
        char: '<',
        reemplazo: 'signo menor que'
    },
    {
        char: '>',
        reemplazo: 'signo mayor que'
    },
    {
        char: '\n',
        reemplazo: 'siguiente línea'
    },
    {
        char: '-',
        reemplazo: 'menos'
    },
    {
        char: '+',
        reemplazo: 'más'
    },
    {
        char: '%',
        reemplazo: 'módulo'
    },
    {
        char: ',',
        reemplazo: 'coma'
    },
    {
        char: '=',
        reemplazo: 'igual'
    },
    {
        char: ':',
        reemplazo: 'dos puntos'
    },
    {
        char: '^',
        reemplazo: 'elevado'
    },
    {
        char: '|',
        reemplazo: 'barra'
    },
    {
        char: '&',
        reemplazo: 'símbolo and'
    },
    {
        char: '!',
        reemplazo: 'cierra exclamación'
    },
    {
        char: '¡',
        reemplazo: 'abre exclamación'
    },
    {
        char: '¿',
        reemplazo: 'abre signo de pregunta'
    },
    {
        char: '?',
        reemplazo: 'cierra signo de pregunta'
    },
    {
        char: '~',
        reemplazo: 'virgulilla'
    },
    {
        char: '#',
        reemplazo: 'signo numeral'
    },
    {
        char: '$',
        reemplazo: 'signo pesos'
    },
    {
        char: '`',
        reemplazo: 'tilde invertida'
    }
];

function reemplazar() {
    let msg = document.getElementById('textoIni').value;
    if (msg == null || msg == '') {
        return;
    }
    let msgfinal = msg;
    reemplazos.forEach(
        objetoReemplazo => {
            rep = objetoReemplazo.char;
            sust = ` ${objetoReemplazo.reemplazo} `;
            msgfinal = msgfinal.replaceAll(rep, sust);
            console.log(msgfinal)
        }
    )
    document.getElementById('textoFin').value = msgfinal;
}

function limpiar() {
    document.getElementById('textoIni').value = '';
    document.getElementById('textoFin').value = '';
}

function copiar() {
    let texto = document.getElementById('textoFin');
    texto.select();
    texto.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(texto.value);
}