 Adobe India Hackathon 2025 – Round 1A Submission

## 📄 Challenge Overview

The goal of Round 1A is to extract a structured outline from PDF files, capturing section headings along with their page numbers and hierarchy levels. The output must conform to a specific JSON schema and must be generated efficiently in a containerized environment.


## 🛠️ Project Structure

round1a/
├── app/
│ ├── extractor.py # Main processing script for heading/title extraction from PDFs
├── input
├── output
├── Dockerfile 
├── sample_dataset
│ ├── pdfs
│ ├── outputs
│ └── schema
│ └── output_schema.json # Output schema definition
└── README.md #you are reading it !!


##Build and Run Instructions

### 1. Build Docker Image

```bash
docker build --platform linux/amd64 -t round1a-extractor.

## 2. How to run?

cd Round1A_folder
docker build --platform=linux/amd64 -t adobe-round1a .

# Run container
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  adobe-round1a
```
## what's needed?
This project requires:

Python 3.10

PyMuPDF (>=1.24)

## Functionality

Automatically reads all .pdf files from /app/input directory.

Extracts outline hierarchy (headings) from each PDF.

Outputs a structured JSON per file in /app/output/.

Output file is named {filename}.json.

## Output Format Example
```
{
  "title": "Minimalist White and Grey Professional Resume",
  "outline": [
    {
      "level": "H3",
      "text": "CERTIFICATIONS",
      "page": 1
    },
    {
      "level": "H1",
      "text": "S H R I M A N T  S H A R M A",
      "page": 1
    }
  ]
}
```
## Validation Checklist

 All input PDFs processed

 JSON file created for each PDF

 Output follows the provided schema

 No internet access during runtime

 Execution time within 10 seconds for 50-page PDFs

 Docker runs on AMD64 CPU only

 All libraries used are open source

 Container reads input as read-only

## Notes

The solution uses Python 3.10

No external internet or cloud-based services used

Designed and tested on Ubuntu 22.04 LTS

## Whats the big thing?

50‑page PDF processing completed in ~3 seconds on Ubuntu + AMD64 CPU.

# Adobe-Deepdoc
This repository contains the complete solutions for Challenge Round 1A and Round 1B of the Adobe India Hackathon 2025.

# Adobe-Deepdoc-round1a-
This repository contains the complete solutions for Challenge Round 1A of the Adobe India Hackathon 2025.

## with regards Shrimant Sharma, Manya Sewkani, Abel Sangeeth 
