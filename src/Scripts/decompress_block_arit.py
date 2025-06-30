import os
import pickle
import sys

# Garante acesso ao diretório "src"
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.insert(0, SRC_DIR)

from Compressor.ArithmeticDecoder import ArithmeticDecoder
from Compressor.SimpleFrequencyTable import SimpleFrequencyTable

# Caminhos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
RESULTS_DIR = os.path.join(BASE_DIR, "Results_Compression")

compressed_path = os.path.join(RESULTS_DIR, "bitstream_compressed.arith")
metadata_path = os.path.join(RESULTS_DIR, "bitstream_arith_metadata.pkl")
output_path = os.path.join(RESULTS_DIR, "reconstructed_output_arith.txt")

# Carregar metadados
with open(metadata_path, "rb") as f:
    metadata = pickle.load(f)

frequencies = metadata["frequencies"]
index_to_symbol = metadata["index_to_symbol"]
num_symbols = metadata["num_symbols"]

# Carregar os bits como inteiros (0 ou 1 por linha)
with open(compressed_path, "r") as f:
    bitstream = [int(line.strip()) for line in f if line.strip() in {"0", "1"}]

# Tabela de frequência
freq_table = SimpleFrequencyTable(frequencies)

# Iterador de bits
def bit_generator(bits):
    for b in bits:
        yield b

bit_iter = bit_generator(bitstream)
decoder = ArithmeticDecoder(32, bit_iter)

# Decodificação
decoded_values = []
for _ in range(num_symbols):
    symbol_idx = decoder.read(freq_table)
    decoded_values.append(index_to_symbol[symbol_idx])

# Escrever resultado
with open(output_path, "w") as f:
    for val in decoded_values:
        f.write(f"{val}\n")

print(f"Decodificação completa: {len(decoded_values)} inteiros reconstruídos.")
print(f"Arquivo salvo em: {output_path}")
