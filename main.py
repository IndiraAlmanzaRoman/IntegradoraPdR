import MiDispositivo
import output

if __name__ == "__main__":
    #Output
    print("Ejecutando MiDispositivo")
    MiDispositivo.guardar_info_dispositivo()
    MiDispositivo.guardar_comando_red()
    print("Proceso MiDispositivo terminado")

    """
    print("Ejecutando main:")
    general_logs.obtener_info_red()
    print("Proceso main terminado")
    """

    print("Ejecutando Output")
    output
    print("Output guardó los datos en device_data.jsonl")
