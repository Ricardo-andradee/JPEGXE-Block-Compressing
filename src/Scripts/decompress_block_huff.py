from dahuffman import HuffmanCodec
import pickle
import os

# Caminhos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
OUTPUT_DIR = os.path.join(BASE_DIR, "Results_Compression")

# Arquivos de entrada
compressed_path = os.path.join(OUTPUT_DIR, "bitstream_compressed.huff")
table_path = os.path.join(OUTPUT_DIR, "bitstream_huffman_table.pkl")

# Arquivo de saída
output_path = os.path.join(OUTPUT_DIR, "reconstructed_output.txt")

# Carregar a tabela de Huffman
with open(table_path, "rb") as f:
    codec: HuffmanCodec = pickle.load(f)

# Ler e decodificar o conteúdo comprimido
with open(compressed_path, "rb") as f:
    compressed_data = f.read()

decoded_integers = codec.decode(compressed_data)

# Salvar a sequência reconstruída
with open(output_path, "w") as f:
    for val in decoded_integers:
        f.write(f"{val}\n")

# Confirmação
print(f"Decompressão completa. {len(decoded_integers)} inteiros reconstruídos para '{output_path}'.")
