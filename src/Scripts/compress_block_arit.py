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
with open(input_path, "r") as f:
    stream = [int(line.strip()) for line in f if line.strip()]

# Contar frequências
counts = Counter(stream)
symbols = sorted(counts.keys())  # símbolos únicos ordenados
frequencies = [counts[s] for s in symbols]

# Símbolos para índices
symbol_to_index = {s: i for i, s in enumerate(symbols)}
indexed_stream = [symbol_to_index[s] for s in stream]

# Tabela de frequência
freq_table = SimpleFrequencyTable(frequencies)

# Codificar em bits
compressed_bits = []
encoder = ArithmeticEncoder(32, compressed_bits.append)
for symbol in indexed_stream:
    encoder.write(freq_table, symbol)
encoder.finish()

# Salvar bits como inteiros
with open(compressed_path, "w") as f:
    for bit in compressed_bits:
        f.write(f"{bit}\n")

# Salvar metadados necessários para decodificação
with open(metadata_path, "wb") as f:
    pickle.dump({
        "frequencies": frequencies,
        "symbols": symbols,  # necessário para reconstruir os valores reais
        "num_symbols": len(indexed_stream)
    }, f)

# Estatísticas
original_size = len(stream) * 8
compressed_size_bits = len(compressed_bits)
compressed_size_bytes = (compressed_size_bits + 7) // 8

print(f"\nOriginal size: {original_size} bytes")
print(f"Compressed size: {compressed_size_bytes} bytes")
print(f"Compression ratio: {compressed_size_bytes / original_size:.2%}")
print(f"Compressed bits saved to: {compressed_path}")
