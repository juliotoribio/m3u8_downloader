import yt_dlp
import os
import subprocess

# Solicitar al usuario el nombre del archivo de salida
filename = input("Introduce el nombre del archivo de salida (sin extensión): ")

# Solicitar al usuario la URL del archivo .m3u8
url = input("Introduce la URL del archivo .m3u8: ")

# Función para validar la URL
def validar_url(url):
    try:
        # Configuraciones para verificar si la URL es válida
        ydl_opts = {
            'quiet': True,  # No mostrar salida detallada
            'simulate': True,  # Simular sin descargar nada
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)  # Intentar extraer información
        return True  # Si no hay errores, la URL es válida
    except Exception as e:
        print(f"URL no válida: {e}")
        return False

# Validar la URL proporcionada
if not validar_url(url):
    print("La URL proporcionada no es válida. Por favor, revisa la URL e inténtalo de nuevo.")
else:
    # Obtener la ruta del directorio donde está el script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Crear una carpeta con el nombre proporcionado por el usuario dentro de la ruta del script
    output_dir = os.path.join(script_dir, filename)
    os.makedirs(output_dir, exist_ok=True)  # Crea la carpeta si no existe

    # Ruta del archivo de salida dentro de la carpeta recién creada
    output_file = os.path.join(output_dir, f"{filename}.mp4")

    # Configuraciones para descargar video y audio, y guardarlo en la nueva carpeta
    ydl_opts = {
        'format': 'bestvideo+bestaudio',  # Descargar el mejor video y audio disponibles
        'outtmpl': output_file,  # Ruta completa en la carpeta recién creada
        'merge_output_format': 'mp4',  # Fusionar ambos en un archivo MP4
    }

    # Descargar el video y fusionar el audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Ruta completa del archivo descargado
    video_path = output_file

    # Comando ffmpeg para cortar el video en partes de 5 minutos
    def split_video(video_path, segment_length=300):  # 300 segundos = 5 minutos
        output_pattern = os.path.join(output_dir, f"{filename}_part_%03d.mp4")  # Guardar segmentos en la misma carpeta
        command = [
            'ffmpeg', '-i', video_path, '-c', 'copy', '-map', '0', 
            '-segment_time', str(segment_length), '-f', 'segment', '-reset_timestamps', '1', output_pattern
        ]
        subprocess.run(command, check=True)

    # Dividir el video en partes de 5 minutos
    split_video(video_path)
