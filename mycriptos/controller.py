#from mycriptos.view import test_input, output
#from mycriptos.models import criptos, fiats, get_rate
#
#class Controller:
#    def mainloop(self):
#        while True:
#            # Usando la Vista para entrada de datos del usuario
#            cripto = test_input(criptos, "Que criptomoneda quieres saber? ")  
#            fiat = test_input(fiats, "En que la quieres? ")
#
#            # Usar el modelo para obtener un dato de internet
#            is_OK, data = get_rate(cripto, fiat)
#
#            # Tendría que ir a la vista, pero todavía no
#            output(is_OK, cripto, fiat, data)
#
#            # Preguntar si seguimos, la pregunta la delegamos en la vista 
#            more_conversions = test_input(('S', 'N'), "Quieres introducir más monedas? ")
#            if more_conversions != "S":
#                break