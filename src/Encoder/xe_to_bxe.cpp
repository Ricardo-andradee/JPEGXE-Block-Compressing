#include <iostream>
#include <fstream>
#include <vector>
#include <cstdlib>
#include <string>
#include <cstdint>
#include <algorithm>
#include "../Codec/xe_format.h" // ajusta para o caminho correto no teu projeto

using namespace XEFormat;

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " INPUT_XE_FILE NUM_EVENTS_TO_READ (0 = ALL)" << std::endl;
        return 1;
    }

    std::ifstream input_file(argv[1], std::ios::binary);
    if (!input_file) {
        std::cerr << "Cannot open input file: " << argv[1] << std::endl;
        return 1;
    }

    int max_events = std::atoi(argv[2]);
    if (max_events < 0) {
        std::cerr << "Invalid number of events to read: " << argv[2] << std::endl;
        return 1;
    }

    const FieldsDefinition fields_def = FieldsDefinition::make_reference();
    const size_t BLOCK_SIZE = 1024;

    std::vector<encoded_event_t> block;
    int total_events_read = 0;
    int block_index = 0;
    bool final_block_created = false;

    // Arquivo de saída para os eventos codificados
    std::ofstream out_file("../../Block_Files/encoded_output.txt");
    if (!out_file) {
        std::cerr << "Cannot open output file for writing.\n";
        return 1;
    }

    while (input_file && (max_events == 0 || total_events_read < max_events)) {
        encoded_event_t encoded_event;

        if (!Decoder::read_next_encoded_event(input_file, fields_def, encoded_event)) break;

        block.push_back(encoded_event);
        ++total_events_read;

        if (block.size() == BLOCK_SIZE) {
            std::sort(block.begin(), block.end());

            std::vector<encoded_event_t> diff_encoded;
            diff_encoded.push_back(block[0]);
            for (size_t i = 1; i < block.size(); ++i) {
                diff_encoded.push_back(block[i] - block[i - 1]);
            }

            for (auto val : diff_encoded) {
                out_file << val << "\n";
            }

            block.clear();
            ++block_index;
        }
    }

    if (!block.empty()) {
        std::sort(block.begin(), block.end());

        std::vector<encoded_event_t> diff_encoded;
        diff_encoded.push_back(block[0]);
        for (size_t i = 1; i < block.size(); ++i) {
            diff_encoded.push_back(block[i] - block[i - 1]);
        }

        for (auto val : diff_encoded) {
            out_file << val << "\n";
        }

        final_block_created = true;
    }

    input_file.close();
    out_file.close();

    // Log final
    std::cerr << "\n--- RESUMO ---\n";
    std::cerr << "Total de eventos lidos: " << total_events_read << "\n";
    std::cerr << "Blocos completos criados: " << block_index << "\n";
    if (final_block_created)
        std::cerr << "Bloco final incompleto também foi gerado.\n";
    else
        std::cerr << "Nenhum bloco final incompleto.\n";

    return 0;
}
