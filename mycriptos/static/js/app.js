var pet_todos = new XMLHttpRequest()

function appendCell(row, data) {
    let the_cell = document.createElement("td")
        row.appendChild(the_cell)
        the_cell.innerHTML = data
}

function muestraTodos(){
    let pedido = this.responseText
    let data = JSON.parse(pedido)
    let the_father= document.querySelector("#table_movements")
    
    for (let i=0; i<data.length; i++){
        let the_row = document.createElement("tr")
        the_father.appendChild(the_row)

        appendCell(the_row, data[i].date)
        appendCell(the_row, data[i].time)
        appendCell(the_row, data[i].moneda_from)
        appendCell(the_row, data[i].cantidad_from)
        appendCell(the_row, data[i].moneda_to)
        appendCell(the_row, data[i].cantidad_to)
    }
    

    
    alert(pedido)
}

window.onload = function() {
    pet_todos.open("GET", "/api/v1/all")
    pet_todos.addEventListener("load", muestraTodos)

    pet_todos.send()
}