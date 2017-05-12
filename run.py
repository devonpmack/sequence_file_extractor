from sequence_getter import SequenceGetter
import sys
import os
import re
import zipfile

import argparse

parser = argparse.ArgumentParser(description="Retrieve fasta and/or fastq files from the NAS")
parser.add_argument('output_folder_name', type=str, help="Name of the folder to put the result files in")
parser.add_argument("-f", "--fasta", action="store_true",
                    help="Retrieve fasta files in fasta_retrieve_list.txt")
parser.add_argument("-q", "--fastq", action="store_true",
                    help="Retrieve fastq files in fastq_retrieve_list.txt")
parser.add_argument("--zip", action="store_true",
                    help="Zip the final results")

args = parser.parse_args()
name = args.output_folder_name

# If bad arguments
if not args.fastq and not args.fasta:
    print("Please use -q (fastq) and/or -f (fasta) to choose what filetype you want to retrieve.")
    parser.print_help()
    exit(1)

script_dir = sys.path[0]
retriever = SequenceGetter(outputfolder=os.path.join(script_dir, 'extract', name))

if args.fastq:
    print("Retrieving fastqs...")

    f = open("fastq_retrieve_list.txt", "r")
    ids = re.findall(r"(2\d{3}-\w{2,10}-\d{3,4})", f.read())
    f.close()

    for seq_id in ids:
        for r in [1,2]:
            retriever.retrieve_file(seq_id, filetype="fastq_R%d" % r)

if args.fasta:
    print("Retrieving fastas...")
    f = open("fasta_retrieve_list.txt", "r")
    ids = re.findall(r"(2\d{3}-\w{2,10}-\d{3,4})", f.read())
    f.close()

    for seq_id in ids:
        retriever.retrieve_file(seq_id, filetype="fasta")

if args.zip:
    # Zip all the files
    p = os.path.join(script_dir, 'extract', name)
    results_zip = os.path.join(p, name + '.zip')
    self.t.time_print("Creating zip file %s" % results_zip)

    try:
        os.remove(results_zip)
    except OSError:
        pass

    zipf = zipfile.ZipFile(results_zip, 'w', zipfile.ZIP_DEFLATED)
    for to_zip in os.listdir(p):
        zipf.write(os.path.join(p, to_zip), arcname=to_zip)
        self.t.time_print("Zipped %s" % to_zip)

    zipf.close()