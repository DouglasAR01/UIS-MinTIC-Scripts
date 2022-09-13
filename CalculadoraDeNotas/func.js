const datos = [
    {
        asignatura: 'Desarrollo de Software',
        porcentaje: 80,
        actividades: [
            {
                nombre: 'Sprint 1: Definiendo el proyecto',
                porcentaje: 18.75
            },
            {
                nombre: 'Sprint 2: Diseñando la base de datos',
                porcentaje: 18.75
            },
            {
                nombre: 'Sprint 3: Estructurando el Backend',
                porcentaje: 31.25
            },
            {
                nombre: 'Sprint 4: Estructurando el frontend',
                porcentaje: 31.25
            }
        ]
    },
    {
        asignatura: 'Inglés III',
        porcentaje: 10,
        actividades: [
            {
                nombre: 'ESP Reading 10',
                porcentaje: 12.5
            },
            {
                nombre: 'ESP Reading 12',
                porcentaje: 12.5
            },
            {
                nombre: 'Academic Reading 10',
                porcentaje: 12.5
            },
            {
                nombre: 'Academic Reading 12',
                porcentaje: 12.5
            },
            {
                nombre: 'Mid-Term Exam',
                porcentaje: 25
            },
            {
                nombre: 'Assessment Test - Cycle 3',
                porcentaje: 25
            }
        ]
    },
    {
        asignatura: 'Habilidades personales III',
        porcentaje: 10,
        actividades: [
            {
                nombre: 'Pitch de Talento',
                porcentaje: 100
            }
        ]
    }
];

function createRow(content = [], id){
    const tabla = document.getElementById('datos');
    row = document.createElement('tr');
    content.forEach(celda => {
        nodo = document.createTextNode(celda);
        cell = document.createElement('td');
        cell.appendChild(nodo);
        row.appendChild(cell);
    });
    nodoNota = document.createElement('input');
    nodoNota.setAttribute('id', id);
    nodoNota.setAttribute('class', 'form-control');
    nodoNota.setAttribute('type', 'number');
    nodoNota.setAttribute('value', 0);
    nodoNota.setAttribute('min', 0);
    nodoNota.setAttribute('max', 5);
    celdaNota = document.createElement('td');
    celdaNota.appendChild(nodoNota);
    row.appendChild(celdaNota);
    tabla.appendChild(row);
}

function createRowR(content = [], id){
    const tabla = document.getElementById('resultados');
    row = document.createElement('tr');
    content.forEach(celda => {
        nodo = document.createTextNode(celda);
        cell = document.createElement('td');
        cell.appendChild(nodo);
        row.appendChild(cell);
    });
    row.lastChild.id = id;
    tabla.appendChild(row);
}

function init(){
    datos.forEach(dato => {
        let band = false;
        let i = 0;
        dato.actividades.forEach(actividad => {
            createRow([
                !band ? dato.asignatura : '',
                actividad.nombre,
                actividad.porcentaje
            ], `${dato.asignatura}-${i}`)
            i++;
            band = true;
        });
        createRowR([dato.asignatura, dato.porcentaje, 0], `r-${dato.asignatura}`);
    });
    createRowR(['Total Ciclo', '', 0], 'r-ciclo')    
}

function calcular(){
    let acum = 0;
    datos.forEach(dato => {
        let notaAsig = 0;
        let i = 0;
        dato.actividades.forEach(actividad => {
            let elem = document.getElementById(`${dato.asignatura}-${i}`)            
            if (elem.value < 0 || elem.value == ''){
                elem.value = 0;
            }
            if (elem.value > 5){
                elem.value = 5;
            }
            let num = elem.value;
            num = parseFloat(num);
            notaAsig += num*(actividad.porcentaje/100);
            i++;
        });
        rAsig = document.getElementById(`r-${dato.asignatura}`);
        rAsig.innerHTML = notaAsig;
        acum += notaAsig*(dato.porcentaje/100);
    });
    document.getElementById('r-ciclo').innerText = acum;
}