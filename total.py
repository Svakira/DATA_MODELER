import subprocess
import os
import requests
import json

def txt_converter(input_file, output_file):
    mp3_files = [file for file in os.listdir(input_file) if file.endswith('.mp3')]
    epub_files = [file for file in os.listdir(input_file) if file.endswith('.epub')]
    file =[file for file in os.listdir(input_file) ]

    for mp3_file in mp3_files:
        mp3_file_path = os.path.join(input_file, mp3_file)
        output_file_path = os.path.join(output_file, f"{os.path.splitext(mp3_file)[0]}.txt")

        with open(mp3_file_path, 'rb') as f:
            response = requests.post('http://207.178.107.92:8080/', files={'data': f})
        
            print(output_file_path)
            print(response)
            print(response.content)
            transcript = ""
            utterances = response.json()
            for utterance in utterances:
                transcript += f"{utterance['text']}\n"
            print(transcript)
            with open(output_file_path, 'w') as output_file:
                output_file.write(transcript)

    for epub_file in epub_files:
        epub_file_path = os.path.join(input_file,epub_file)
        output_file_path = os.path.join(output_file, f"{os.path.splitext(epub_file)[0]}.txt")
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
        except subprocess.CalledProcessError as e:
            print(f'Error durante la conversión: {e}')
    

if __name__ == "__main__":
    # Replace 'source_folder_path' with the path to your source folder
    input_file = "C:/Users/Sara Cardona/OneDrive/Escritorio/Bible Project_NC"
    # Replace 'destination_file_path' with the desired destination JSONL file path
    output_file = "C:/Users/Sara Cardona/OneDrive/Escritorio/Bible Project_NC"

    txt_converter(input_file, output_file)
    print("Text files cleaned, converted to JSONL, and merged successfully! in the path "+output_file)
