from pathlib import Path
import polars as pl
import logging
import typer
from typing_extensions import Annotated
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

def read_fasta_to_dict(filepath: Path) -> dict[str, str]:
    """Reads a FASTA-formatted file into a python dictionary

    Args:
        filepath (Path): The path to the fasta file

    Returns:
        dict[str, str]: A dictionary where the sequence IDs are the keys, and the sequences are the values
    """

    fasta_string_lines = open(filepath, "r").readlines()

    sequences = {}
    header = ""
    for line in fasta_string_lines:
        line = line.strip()
        if line.startswith(">"):
            header = line.strip().strip(">")
            if header in sequences:
                logging.warning(
                    f"There is already a line with the header {header} and it will be overwritten"
                )
            sequences[header] = ""
        else:
            sequences[header] += line.strip()

    return sequences

def process_read_names(names: list[str]) -> pl.DataFrame:
    df = pl.DataFrame({"raw_name": names})
    df = df.with_columns(split_name=pl.col("raw_name").str.split("_"))

    df = df.with_columns(
        lineage=pl.col("split_name").list.get(-1),
        timepoint=pl.col("split_name").list.get(2),
        umi=pl.col("split_name").list.get(-2).str.slice(5, 8),
    )

    all_timepoints = sorted(df["timepoint"].unique().to_list())
    all_lineages = sorted(df["lineage"].unique().to_list())

    df = df.with_columns(
        lineage_num=pl.col("lineage").map_elements(
            lambda x: all_lineages.index(x) + 1, return_dtype=int
        ),
        timepoint_num=pl.col("timepoint").map_elements(
            lambda x: all_timepoints.index(x) + 1, return_dtype=int
        ),
    )

    df = df.with_columns(
        new_names=pl.col("umi") + "_tp" + pl.col("timepoint_num").cast(str)
    )

    return df.select(pl.col("new_names", "lineage_num", "lineage"))


def main(input_file: Path,
         output_file: Path):
    
    logging.info(f"Reading {input_file}")
    in_seqs = read_fasta_to_dict(input_file)
    
    logging.info("Processing names.")
    processed_names = process_read_names(list(in_seqs.keys()))
    
    logging.info(f"Writing to {output_file}")
    processed_names.write_csv(output_file)
    
    logging.info("Done.")


def main_cli(input_file: Annotated[Path, typer.Argument(help="Path to the FASTA file that contians the sequence names to process")],
             output_file: Annotated[Path, typer.Argument(help=f"Path to write the resulting CSV file to.")]):
    """Processes a FASTA file into a CSV file allowing Mupundu to colour a highlighter plot by lineage.
    
    
    More explicitly, this program takes as input a FASTA file with unformatted names of the form `X_Y_INT_NNNNNNNN_A` where `X` and 
    `Y` are irrelevant, `INT` is a timepoint identifier, `NNNNNNNN` is an 8-nt UMI and `A` is a lineage identifier. 
    
    
    These sequence names are then converted to the expected Mupundu convention (NNNNNNNN_TP[INT]; [INT] is the timepoitn number),
    and output in a csv table where the two additional columns are lineage number and lineage name.
    """
    
    if not input_file.exists():
        logging.error("Input file doesn't exist. Exiting.")
        exit(1)
    
    if output_file.exists():
        logging.warning("Output file exists, overwriting")
        
    if output_file.is_dir():
        logging.error("Output must be a file. Exiting.")
        exit(1)
        
    if not output_file.suffix.lower() == ".csv":
        logging.warning(f"The output you specified is a {output_file.suffix} file. This won't change the output, we will still write a CSV, but you should consider supplying a CSV file as the output file.")
    
    main(input_file, output_file)   

def cli_entrypoint():
    typer.run(main_cli)

if __name__ == "__main__":
    cli_entrypoint()
