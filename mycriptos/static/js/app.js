function appendCell(row, data) {
    let the_cell = document.createElement("td")
        row.appendChild(the_cell)
        the_cell.innerHTML = data
}

function clearForm() {
    // Limpiar el contenido del formulario después de una inserción exitosa
    document.querySelector("#moneda_from").value = "";
    document.querySelector("#moneda_to").value = "";
    document.querySelector("#cantidad_from").value = "";
    document.querySelector("#calculated_amount").value = "";
}

function process_insert(data) {
    if (data.status == "success") {
        // Llama a la función que obtiene todos los movimientos y actualiza la tabla
        fetch("/api/v1/movimientos")
            .then(convert_to_json)
            .then(all_movements)
            .then(clearForm)
            .catch(process_error)
    } else {
        alert("Error en insercion")
    }
}

function saveMovement(moneda_from, cantidad_from, moneda_to, cantidad_to) {

    let data = {
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

    fetch("/api/v1/movimiento", options)
        .then(convert_to_json)
        .then(process_insert)
        .catch(process_error)

}

function validateMovement(event) {
    event.preventDefault()

    let moneda_from = document.querySelector("#moneda_from").value
    let moneda_to = document.querySelector("#moneda_to").value
    let cantidad_from = document.querySelector("#cantidad_from").value
    let cantidad_to = document.querySelector("#calculated_amount").value

    if (cantidad_from <= 0) {
        alert("La cantidad debe ser positiva")
        return
    }
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

function calculateConversion(event) {
    event.preventDefault()
    let moneda_from = document.querySelector("#moneda_from").value
    let moneda_to = document.querySelector("#moneda_to").value
    let cantidad_from = document.querySelector("#cantidad_from").value
    // Realizar una solicitud a la API para obtener la tasa de cambio
    fetch(`/api/v1/tasa/${moneda_from}/${moneda_to}/${cantidad_from}`)
        .then(convert_to_json)
        .then(data => {
            if (data.status == "success") {
                const rate = data.rate;
                const cantidad_to = (parseFloat(cantidad_from) * rate).toFixed(4); // Redondear a 4 decimales
                // Mostrar el resultado en el elemento "calculated_amount"
                const calculatedAmountElement = document.getElementById("calculated_amount");
                calculatedAmountElement.innerHTML = ` ${cantidad_to} `;
            } else {
                alert("Error al obtener la tasa de cambio");
            }
        })
        .catch(process_error);        
}

window.onload = function() {
    fetch("/api/v1/movimientos")
        .then(convert_to_json)
        .then(all_movements)
        .catch(process_error)

    // Asociar click a enviar formulario al servidor (alta de movimiento)
    document.querySelector("#submit").addEventListener("click", validateMovement) 

    // Agregar evento al botón "submitConversion"
    document.querySelector("#submitConversion").addEventListener("click", calculateConversion);
    
    

}