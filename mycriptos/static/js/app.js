function appendCell(row, data) {
    let the_cell = document.createElement("td")
        row.appendChild(the_cell)
        the_cell.innerHTML = data
}

function process_insert(data) {
    if (data.status == "success") {
        fetch("/api/v1/movimientos",)
            .then(convert_to_json)
            .then(all_movements)
            .catch(process_error)
    } else {
        alert("Error en insercion")
    }
      
}

function saveMovement(moneda_from, cantidad_from, moneda_to, cantidad_to) {
    
    
    let now = new Date(); // obtener fecha y hora actual

    let data = {
        date: now.toISOString().slice(0,10), // formato YYYY-MM-DD
        time: now.toTimeString().slice(0,8),  // formato HH:MM:SS
        moneda_from: moneda_from,
        cantidad_from: cantidad_from, 
        moneda_to: moneda_to,
        cantidad_to: cantidad_to
    } 

    let options = {
        body: JSON.stringify(data),
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    }

    fetch("/api/v1/insert", options)
        .then(convert_to_json)
        .then(process_insert)
        .catch(process_error)

}

function validateMovement(event) {
    event.preventDefault()

 /* let _date = document.querySelector("#date").value
    let today = new Date().toISOString().slice(0, 10)
    if (_date > today) {
        alert("La fecha debe ser hoy o menor")
        return
    }

    let abstract = document.querySelector("#abstract").value
    if (abstract.length < 5) {
        alert("El concepto debe tener al menos 5 caracteres")
        return
    }*/

    let cantidad_from = document.querySelector("#cantidad_from").value
    if (cantidad_from == 0) {
        alert("La cantidad debe ser positiva ")
        return
    }

    let moneda_from = document.querySelector("#moneda_from").value

    saveMovement(moneda_from, cantidad_from, moneda_to, cantidad_to)
}

function convert_to_json(response) {
    return response.json()
}


function all_movements(data) {
    if (data.status = "success") {
        let the_father = document.querySelector("#table_movements_body")
        the_father.innerHTML = ""

        regs = data.data 

        for (let i=0; i < regs.length; i++) {
            let the_row = document.createElement("tr")
            the_father.appendChild(the_row)

            appendCell(the_row, regs[i].date)
            appendCell(the_row, regs[i].time)
            appendCell(the_row, regs[i].moneda_from)
            appendCell(the_row, regs[i].cantidad_from)
            appendCell(the_row, regs[i].moneda_to)
            appendCell(the_row, regs[i].cantidad_to)
        }
    } else {
        alert ("Se ha producido el error " + data.data)
    }
    
}


function process_error(error) {
    alert("Se ha producido el siguiente error: " + error)
}

window.onload = function() {
    fetch("/api/v1/movimientos")
        .then(convert_to_json)
        .then(all_movements)
        .catch(process_error)

    // Asociar clic a enviar formulario al servidor (alta de movimiento)
    document.querySelector("#submit").addEventListener("click", validateMovement) 
}