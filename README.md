# Mupundu Script

Tool to create a CSV file with lineages as numbers, from a FASTA file. For example:

| new_names    | lineage_num | lineage |
| ------------ | ----------- | ------- |
| NNNNNNNN_TP2 | 2           | mx3     |
| NNNNNANN_TP2 | 2           | mx3     |
| BNNNNNNN_TP1 | 1           | mx1     |

## Installing

First, install `uv`: [uv install instructions](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)

Then run:

```shell
uv tool install git+https://github.com/HIVDiversity/mupundu_lineage_script
```

This will install the command-line command `create-lineage-csv`. 

## Usage

You can run `create-lineage-csv --help` to get the following help message:

```text
Usage: create-lineage-csv [OPTIONS] INPUT_FILE OUTPUT_FILE                                                                                                        
                                                                                                                                                                   
 Processes a FASTA file into a CSV file allowing Mupundu to colour a highlighter plot by lineage.                                                                  
 More explicitly, this program takes as input a FASTA file with unformatted names of the form `X_Y_INT_NNNNNNNN_A` where `X` and  `Y` are irrelevant, `INT` is a   
 timepoint identifier, `NNNNNNNN` is an 8-nt UMI and `A` is a lineage identifier.                                                                                  
 These sequence names are then converted to the expected Mupundu convention (NNNNNNNN_TP[INT]; [INT] is the timepoitn number), and output in a csv table where the 
 two additional columns are lineage number and lineage name.                                                                                                       
                                                                                                                                                                   
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    input_file       PATH  Path to the FASTA file that contians the sequence names to process [default: None] [required]                                       │
│ *    output_file      PATH  Path to write the resulting CSV file to. [default: None] [required]                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## License

This work is licensed under the MIT licence, and can be found in the LICENSE.md file.