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
        const mensajeError = document.querySelector('#mensajeError');
        mensajeError.textContent = 'Error en la inserción';

        setTimeout(function() {
         mensajeError.textContent = '';
        }, 5000); // Borrar el mensaje de error después de 5 segundos
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

    if (moneda_from === moneda_to) {
        const mensajeError = document.querySelector('#mensajeError');
        mensajeError.textContent = 'Las monedas no pueden ser iguales';
        setTimeout(function() {
         mensajeError.textContent = '';
        }, 5000); // Borrar
        return
    }
    
    if (cantidad_from <= 0 || cantidad_from === '') {
        const mensajeError = document.querySelector('#mensajeError');
        mensajeError.textContent = 'La cantidad debe ser positiva';
        
        setTimeout(function() {
         mensajeError.textContent = '';
        }, 5000); // Borrar
        return
    }
    if (cantidad_to === '' || cantidad_to === '\n                    ') {
        const mensajeError = document.querySelector('#mensajeError');
        mensajeError.textContent = 'Debe de haber conversión';

        setTimeout(function() {
          mensajeError.textContent = '';
        }, 5000); // Borrar
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
        const mensajeError = document.querySelector('#mensajeError');
        mensajeError.textContent = 'Se ha producido el error ' + data.data;

        setTimeout(function() {
         mensajeError.textContent = '';
        }, 5000); // Borrar
    }
    
}

function process_error(error) {
    const mensajeError = document.querySelector('#mensajeError');
    mensajeError.textContent = 'Se ha producido el siguiente error: ' + error;

    setTimeout(function() {
     mensajeError.textContent = '';
    }, 5000); // Borrar el mensaje
}

// resetear el valor de 'calculated_amount'
function resetCalculatedAmount() {
    const calculatedAmountElement = document.getElementById("calculated_amount");
    calculatedAmountElement.innerHTML = '';
}

function calculateConversion(event) {
    event.preventDefault()
    
    let moneda_from = document.querySelector("#moneda_from").value
    let moneda_to = document.querySelector("#moneda_to").value
    let cantidad_from = document.querySelector("#cantidad_from").value

    if (cantidad_from ==='') {
        const mensajeError = document.querySelector('#mensajeError');
        mensajeError.textContent = 'Especificar cantidad';
        setTimeout(function() {
         mensajeError.textContent = '';
        }, 5000); // Borrar
        return
    }
    if (moneda_from === moneda_to) {
        const mensajeError = document.querySelector('#mensajeError');
        mensajeError.textContent = 'Las monedas no pueden ser iguales';
        setTimeout(function() {
         mensajeError.textContent = '';
        }, 5000); // Borrar
        return
    }
    if (moneda_from === '') {
        const mensajeError = document.querySelector('#mensajeError');
        mensajeError.textContent = 'Selecciona moneda_from';
        
        setTimeout(function() {
         mensajeError.textContent = '';
        }, 5000); // Borrar
        return
    }
    if (moneda_to === '' ) {
        const mensajeError = document.querySelector('#mensajeError');
        mensajeError.textContent = 'Selecciona moneda_to';

        setTimeout(function() {
          mensajeError.textContent = '';
        }, 5000); // Borrar
        return
    }
    // Realizar una solicitud a la API para obtener la tasa de cambio
    fetch(`/api/v1/tasa/${moneda_from}/${moneda_to}/${cantidad_from}`)
        .then(convert_to_json)
        .then(data => {
            if (data.status == "success") {
                const rate = data.rate;
                const cantidad_to = (parseFloat(cantidad_from) * rate).toFixed(8); // Redondear a 8 decimales
                // Mostrar el resultado en el elemento "calculated_amount"
                const calculatedAmountElement = document.getElementById("calculated_amount");
                calculatedAmountElement.innerHTML = ` ${cantidad_to} `;
            } else {
                const mensajeError = document.querySelector('#mensajeError');
                mensajeError.innerHTML = 'Error al obtener la tasa de <br> cambio: ' + data.data;

                setTimeout(function() {
                  mensajeError.innerHTML = '';
                }, 5000); // Borrar el mensaje de error después de 5 segundos
            }
        })
        .catch(process_error);        
}

function getStatus() {
    fetch("/api/v1/status")
        .then(convert_to_json)
        .then(data => {
            if (data.status === "success") {
                const statusSection = document.getElementById("statusSection");
                const cryptoList = document.getElementById("cryptoList");
                const portfolioValue = document.getElementById("portfolioValue");



                // Calcular el resultado (suma de valor actual y precio de compra)
                const resultadohtml = (data.data.actual_value + data.data.price).toFixed(2);

                // Mostrar el estado de la inversión
                portfolioValue.innerHTML = `Valor actual: ${data.data.actual_value.toFixed(2)} €<br>
                Precio de compra: ${data.data.price.toFixed(2)} €<br>
                Resultado: ${resultadohtml} €`;


                // Mostrar la lista de cryptomonedas con su balance y value
                cryptoList.innerHTML = "<h3>Estado de la inversión:</h3>";
                const table = document.createElement("table");
                table.innerHTML = `
                    <tr>
                        <th>Cantidad en tu wallet</th>
                        <th>Crypto Moneda</th>
                        <th>Valor en €</th>
                    </tr>
                `;
                for (const [moneda, info] of Object.entries(data.data.wallet)) {
                    if (moneda !== "EUR") {
                        const row = document.createElement("tr");
                        row.innerHTML = `
                            <td>${info.balance.toFixed(8)}</td>
                            <td>${moneda}</td>
                            <td>${info.value.toFixed(8)}</td>
                        `;
                        table.appendChild(row);
                    }
                }
                cryptoList.appendChild(table);

                statusSection.classList.remove("invisible");
            } else {
                const mensajeError = document.querySelector('#mensajeError');
                mensajeError.textContent = 'Error al obtener el estado de la inversión';

                setTimeout(function() {
                  mensajeError.textContent = '';
                }, 5000); // Borrar el mensaje de error después de 5 segundos
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
    
    // Agregar evento al botón "statusButton" para obtener el estado de la inversión
    document.querySelector("#statusButton").addEventListener("click", getStatus); 

    // Agregar controlador de evento 'change' a los elementos de selección de moneda
    document.querySelector("#moneda_from").addEventListener('change', resetCalculatedAmount);
    document.querySelector("#moneda_to").addEventListener('change', resetCalculatedAmount);
    document.querySelector("#cantidad_from").addEventListener('change', resetCalculatedAmount);
}