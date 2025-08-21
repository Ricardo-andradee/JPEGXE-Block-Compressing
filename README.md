# Block-Based Compression of Event-Based Data Using Huffman and Arithmetic Coding

## Overview

This repository presents a **lossless coding** solution for event-based vision data stored in JPEG XE’s `.xe` format. The proposed method introduces a **block-based transformation** that reorganizes the event stream into **fixed-size blocks**, preparing the data for efficient statistical compression.

### Processing Pipeline

1. **Event Reading**  
   Encoded events from the `.xe` file are read sequentially using the dedicated JPEG XE decoder.

2. **Block Segmentation**  
   Events are accumulated into **fixed-size blocks** (default: 1024 events per block). Each block is processed as soon as it reaches the target size.

3. **In-Block Sorting**  
   Events within the block are sorted to reduce entropy and improve subsequent compression efficiency.

4. **Differential Encoding**  
   Within each block, the first event is kept as-is, and subsequent events are replaced by the **difference from the previous event**.  
   This transformation reduces value variability, making the data more predictable for Huffman or Arithmetic coding.

5. **Output Writing**  
   The processed blocks are written sequentially to an output file (`encoded_output.txt`) after sorting and differential encoding.  
   The **block structure exists in memory during processing**.

6. **Global Compression**  
   After preprocessing, we compressed using:
   - **Huffman coding**, or  
   - **Arithmetic coding**  

   Global compression avoids the overhead of generating separate tables per block while still maintaining the conceptual block structure for experimentation.

### Goal

The main goal of this work is to evaluate whether **block-based organization with differential encoding** enables more efficient statistical compression of event-based vision data. This implementation also provides a foundation for further experimentation and contributions to JPEG XE standardization efforts.



## Reference JPEG XE Repository
In the link below is available the source code for the JPEG XE standardization activity (raw canonical XE format):

- [JPEG XE Source Code](https://gitlab.com/wg1/jpegxe/ctc_tools)

## Reference Dataset
In the repository there are some sample datasets, but the link below provides access to the full JPEG XE reference dataset in canonical format:

- [JPEG XE Reference Dataset](https://nx51932.your-storageshare.de/s/QgNjbps8dgAaCJ7)

## Reference Arithmetic Coding Repository  
The arithmetic encoder and decoder used in this project are based on publicly available educational implementations of static arithmetic coding:

- [Reference Arithmetic Coding Source (Nayuki)](https://github.com/nayuki/Reference-arithmetic-coding)

## Compiling the Software

### Requirements
**C++17 Compiler**  
You need to install a C++ compiler with support for C++17; depending on your operating system the instructions may differ.

**System compatible with UNIX commands**  
Linux, macOS, or Windows with WSL are recommended.

**Python 3.6+**  
The compression and decompression scripts are written in Python.

**Required Python packages:**
- `dahuffman` — for static Huffman coding
- `pickle`, `os`, `sys` — standard Python libraries

You can install `dahuffman` via pip:

```bash
pip install dahuffman
```

## Running Test Scripts

### On Linux

Run the following commands in the project directory:

```sh
cd Encoder
g++ -std=c++17 -O2 xe_to_blockxe.cpp ../Codec/xe_format.cpp -o xe_to_blockxe
```

To run the encoder:

```sh
./xe_to_blockxe ../../Datasets/"dataset_name".xe 0 
```

Use `0` to process the full file or provide a specific number of events to read.

Run the Huffman compression/decompression:

```sh
cd Scripts
python3 compress_block_huff.py
python3 decompress_block_huff.py
```

Run the Arithmetic compression/decompression:

```sh
cd Scripts
python3 compress_block_arit.py
python3 decompress_block_arit.py

```


