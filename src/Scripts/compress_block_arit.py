import os
import pickle
from collections import Counter
import sys

# Garante que a pasta "src" está no path
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, SRC_DIR)

# Importar módulos Nayuki
from Compressor.ArithmeticEncoder import ArithmeticEncoder
from Compressor.SimpleFrequencyTable import SimpleFrequencyTable

# Caminhos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_DIR = os.path.join(BASE_DIR, "Block_Files")
OUTPUT_DIR = os.path.join(BASE_DIR, "Results_Compression")

input_path = os.path.join(DATA_DIR, "encoded_output.txt")
compressed_path = os.path.join(OUTPUT_DIR, "bitstream_compressed.arith")
metadata_path = os.path.join(OUTPUT_DIR, "bitstream_arith_metadata.pkl")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Ler entrada
bitstream = []
with open(input_path, "r") as f:
    for line in f:
        line = line.strip()
        if line:
            bitstream.append(int(line))

# Mapear inteiros para índices sequenciais (necessário para codificação por símbolo)
symbols = sorted(set(bitstream))
symbol_to_index = {s: i for i, s in enumerate(symbols)}
index_to_symbol = {i: s for s, i in symbol_to_index.items()}
indexed_stream = [symbol_to_index[x] for x in bitstream]

# Frequência por símbolo (mínimo 1)
num_symbols = len(symbols)
frequencies = [1] * num_symbols  # Inicializa com 1 para evitar zero
counts = Counter(indexed_stream)
for idx, freq in counts.items():
    frequencies[idx] = freq

# Tabela de frequência
freq_table = SimpleFrequencyTable(frequencies)

# Codificar em bits
compressed_bits = []
bitout = compressed_bits.append
encoder = ArithmeticEncoder(32, bitout)

for symbol in indexed_stream:
    encoder.write(freq_table, symbol)
encoder.finish()

# Salvar bits como inteiros (0 ou 1 por linha)
with open(compressed_path, "w") as f:
    for bit in compressed_bits:
        f.write(f"{bit}\n")

# Salvar metadados necessários para decodificação
with open(metadata_path, "wb") as f:
    pickle.dump({
        "symbol_to_index": symbol_to_index,
        "index_to_symbol": index_to_symbol,
        "frequencies": frequencies,
        "num_symbols": len(indexed_stream)
    }, f)

# Estatísticas
original_size = len(bitstream) * 8  # cada int64 = 8 bytes
compressed_size_bits = len(compressed_bits)
compressed_size_bytes = (compressed_size_bits + 7) // 8

print(f"Original size: {original_size} bytes")
print(f"Compressed size: {compressed_size_bytes} bytes")
print(f"Compression ratio: {compressed_size_bytes / original_size:.2%}")
print(f"Compressed bits saved to: {compressed_path}")
