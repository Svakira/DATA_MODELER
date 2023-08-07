import subprocess
import os
import requests
import json
from pytube import YouTube

def download_youtube_audio(youtube_url, output_folder):
    try:
        youtube = YouTube(youtube_url)
        audio_stream = youtube.streams.filter(only_audio=True, file_extension='mp4').first()
        audio_stream.download(output_folder)
        # Renombrar el archivo descargado con la extensión .mp3
        original_file_path = os.path.join(output_folder, audio_stream.default_filename)
        mp3_file_path = os.path.splitext(original_file_path)[0] + ".mp3"
        os.rename(original_file_path, mp3_file_path)
        print("Audio descargado exitosamente en formato MP3.")
    except Exception as e:
        print(f"Error al descargar el audio: {e}")

def txt_converter(input_file, output_folder):
    mp3_files = [file for file in os.listdir(input_file) if file.endswith('.mp3')]
    epub_files = [file for file in os.listdir(input_file) if file.endswith('.epub')]

    #mp3 to txt 
    for mp3_file in mp3_files:
        mp3_file_path = os.path.join(input_file, mp3_file)
        output_file_path = os.path.join(output_folder, f"{os.path.splitext(mp3_file)[0]}.txt")

        with open(mp3_file_path, 'rb') as f:
            response = requests.post('http://portdev.massedcompute.com:8080/', files={'data': f})
        
            transcript = ""
            utterances = response.json()
            for utterance in utterances:
                transcript += f"{utterance['text']}\n"
            
            with open(output_file_path, 'w') as output_file:
                output_file.write(transcript)

        # Remove the old MP3 file
        os.remove(mp3_file_path)
    #epub to txt
    for epub_file in epub_files:
        epub_file_path = os.path.join(input_file, epub_file)
        output_file_path = os.path.join(output_folder, f"{os.path.splitext(epub_file)[0]}.txt")
        
        try:
            subprocess.run([
                'ebook-convert',
                epub_file_path,
                output_file_path,
                '--txt-output-formatting=plain',  # Para que el TXT no tenga formato adicional
                '--smarten-punctuation',  # Para mejorar la puntuación en el TXT
                '--disable-font-rescaling'  # Deshabilitar el redimensionamiento de fuentes
            ], check=True)

            print(f'Conversión exitosa. El archivo TXT se ha guardado en: {output_file_path}')

            # Remove the old EPUB file
            os.remove(epub_file_path)

        except subprocess.CalledProcessError as e:
            print(f'Error durante la conversión: {e}')
    
def clean_text(file_path):
    with open(file_path, 'r', encoding='latin-1') as f:
        lines = f.readlines()

    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(cleaned_lines)

def clean_all_txt_files(output_folder):
    txt_files = [file for file in os.listdir(output_folder) if file.endswith('.txt')]
    
    for txt_file in txt_files:
        txt_file_path = os.path.join(output_folder, txt_file)
        cleaned_text = clean_text(txt_file_path)

        with open(txt_file_path, 'w',encoding='latin-1') as txt_output_file:
            txt_output_file.write(cleaned_text)

     

if __name__ == "__main__":
    # Replace 'source_folder_path' with the path to your source folder
    input_file = "C:/Users/Sara Cardona/OneDrive/Escritorio/Bible Project_NC"
    # Replace 'destination_folder_path' with the desired destination directory path for converted files
    output_folder = "C:/Users/Sara Cardona/OneDrive/Escritorio/Bible Project_NC"

    youtube_url = "https://www.youtube.com/watch?v=RY31fCtbQgw"
    download_youtube_audio(youtube_url, output_folder)

    # Ensure the output_folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    txt_converter(input_file, output_folder)

    # Clean all the text files in the output folder
    clean_all_txt_files(output_folder)

    print("Text files cleaned, converted to JSONL, and merged successfully! in the path " + output_folder)
