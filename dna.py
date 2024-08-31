import pandas as pd
import streamlit as st
import altair as alt
from collections import Counter


st.write("""
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA using a simulated MapReduce approach!

***
""")


st.header('Enter DNA sequence')

sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

# Read sequence input
sequence = st.text_area("Sequence input", sequence_input, height=250)
sequence = sequence.splitlines()
sequence = sequence[1:]  # Skips the sequence name (first line)
sequence = ''.join(sequence)  # Concatenates list to string

# Convert sequence to uppercase
sequence = sequence.upper()

st.write("""
***
""")

## Prints the input DNA sequence
st.header('INPUT (DNA Query)')
sequence

## MapReduce functions
def map_function(chunk):
    # Produce (nucleotide, 1) pairs for a chunk of sequence
    return [(nucleotide, 1) for nucleotide in chunk]

def reduce_function(mapped_data):
    # Aggregate counts from (nucleotide, 1) pairs
    counter = Counter()
    for nucleotide, count in mapped_data:
        counter[nucleotide] += count
    return dict(counter)

def split_sequence(seq, chunk_size):
    # Split the sequence into chunks
    return [seq[i:i + chunk_size] for i in range(0, len(seq), chunk_size)]

# Simulate MapReduce
chunk_size = len(sequence) // 10 + 1  # Split sequence into chunks
chunks = split_sequence(sequence, chunk_size)

# Map phase
mapped_results = []
for chunk in chunks:
    mapped_results.extend(map_function(chunk))

# Reduce phase
reduced_data = reduce_function(mapped_results)

## DNA nucleotide count
st.header('OUTPUT (DNA Nucleotide Count)')

### 1. Print dictionary
st.subheader('1. Print dictionary')
X = reduced_data
X

### 2. Print text
st.subheader('2. Print text')
st.write('There are  ' + str(X.get('A', 0)) + ' adenine (A)')
st.write('There are  ' + str(X.get('T', 0)) + ' thymine (T)')
st.write('There are  ' + str(X.get('G', 0)) + ' guanine (G)')
st.write('There are  ' + str(X.get('C', 0)) + ' cytosine (C)')

### 3. Display DataFrame
st.subheader('3. Display DataFrame')
df = pd.DataFrame.from_dict(X, orient='index')
df = df.rename({0: 'count'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns={'index': 'nucleotide'})
st.write(df)

### 4. Display Bar Chart using Altair
st.subheader('4. Display Bar chart')
p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)
p = p.properties(
    width=alt.Step(80)  # controls width of bar.
)
st.write(p)


### FOR THIS MAP REDUCE IS DONE IN SAME FILE ###########