from dahuffman import HuffmanCodec
import pickle
import os
from collections import Counter

# Caminhos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_DIR = os.path.join(BASE_DIR, "Block_Files")  # ajuste se necessário
OUTPUT_DIR = os.path.join(BASE_DIR, "Results_Compression")

# Arquivos
input_path = os.path.join(DATA_DIR, "encoded_output.txt")
compressed_path = os.path.join(OUTPUT_DIR, "bitstream_compressed.huff")
table_path = os.path.join(OUTPUT_DIR, "bitstream_huffman_table.pkl")

# Criar diretório de saída, se não existir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Leitura dos inteiros do arquivo
bitstream = []
with open(input_path, "r") as f:
    for line in f:
        line = line.strip()
        if line:
            bitstream.append(int(line))

# Criar codec e codificar a sequência de inteiros
codec = HuffmanCodec.from_data(bitstream)
compressed = codec.encode(bitstream)

# Salvar o conteúdo comprimido
with open(compressed_path, "wb") as f:
    f.write(compressed)

# Salvar a tabela de Huffman
with open(table_path, "wb") as f:
    pickle.dump(codec, f)

# Estatísticas
original_size = len(bitstream) * 8  # 8 bytes por int64
compressed_size = len(compressed)

print(f"Original size: {original_size} bytes")
print(f"Compressed size: {compressed_size} bytes")
print(f"Compression ratio: {compressed_size / original_size:.2%}")

# Análise da frequência de símbolos
symbol_counts = Counter(bitstream)
symbol_codes = codec.get_code_table()

print("\nTop 10 most frequent symbols and their Huffman codes:")
print("Symbol       | Frequency | Huffman Code")
for symbol, freq in symbol_counts.most_common(10):
    print(f"{symbol:<12} | {freq:<9} | {symbol_codes[symbol]}")
