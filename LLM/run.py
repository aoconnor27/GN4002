from glob import glob
from sys import argv
from os import system, path, makedirs
import pandas as pd
from multiprocessing import Pool
from functools import partial

MODELS = ( "phi3", "phi3:14b", "gemma2", "gemma2:27b")# "llama3.1", "llama3.2", "mistral",
TEMPERATURES = (0.2,0.6, 1.0)
MAX_TOKENS = (500, 1000, 1500)
questions = pd.read_csv(argv[2])

def run_f(fl, model, temp, tokens,output, query):
    output_time = f"{output}/{query[0]}.time"
    print(
                       f"/usr/bin/time -vo {output_time} ./metallmcpu -c {fl} -n {query[0]} -q \"{query[1]}\" -o {output} -m {model} -t {temp} -x {tokens}"
                        # f"./metallmcpu -c {fl} -n {row['QN']} -q {row['Question']} -o {output} -m {model} -t {temp} -x {tokens}"
                    )

    system(
                       f"/usr/bin/time -vo {output_time} ./metallmcpu -c {fl} -n {query[0]} -q \"{query[1]}\" -o {output} -m {model} -t {temp} -x {tokens}"
                        # f"./metallmcpu -c {fl} -n {row['QN']} -q {row['Question']} -o {output} -m {model} -t {temp} -x {tokens}"
                    )


for fl in glob(f"{argv[1]}/*.csv"):
    csvname = path.split(fl)[1].split(".csv")[0]
    for model in MODELS:
        for temp in TEMPERATURES:
            for tokens in MAX_TOKENS:
                output = f"{argv[3]}/{csvname}_{model.replace('.','').replace(':','')}_{temp}_{tokens}"
                if not path.exists(output):
                    makedirs(output)
                print(output)
                query = []
                for _, row in questions.iterrows():
                    query.append([row['QN'], row["Question"]])
                pf = partial(run_f, fl, model, temp, tokens, output)
                p = Pool(2)
                if model == "gemma2:27b":
                    p = Pool(1)
                p.map(pf, query)
                    
