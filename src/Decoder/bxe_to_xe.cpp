#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstdint>
#include <cstdlib>
#include "../Codec/xe_format.h"  // Ajuste conforme a estrutura do projeto

using namespace XEFormat;

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Use: " << argv[0] << " encoded_output.txt output_file.xe" << std::endl;
        return 1;
    }

    std::ifstream in_file(argv[1]);
    if (!in_file) {
        std::cerr << "Erro ao abrir arquivo de entrada: " << argv[1] << std::endl;
        return 1;
    }

    std::ofstream out_file(argv[2], std::ios::binary);
    if (!out_file) {
        std::cerr << "Erro ao criar arquivo de saída: " << argv[2] << std::endl;
        return 1;
    }

    const FieldsDefinition fields_def = FieldsDefinition::make_reference();

    std::string line;
    encoded_event_t previous = 0;
    int count = 0;

    while (std::getline(in_file, line)) {
        if (line.empty()) continue;

        encoded_event_t delta = std::stoll(line);
        encoded_event_t current = (count == 0) ? delta : previous + delta;

        Encoder::write_encoded_event(out_file, fields_def, current);
        if (!out_file.good()) {
            std::cerr << "Erro ao escrever evento no arquivo de saída.\n";
            return 1;
        }

        previous = current;
        ++count;
    }

    in_file.close();
    out_file.close();

    std::cerr << "Reconstrução concluída: " << count << " eventos salvos em " << argv[2] << std::endl;
    return 0;
}
