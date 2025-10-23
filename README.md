# SciSciNet Explorer

A user-friendly GUI application for exploring and analyzing scientific publications using SciSciNet and OpenAlex data.

## Overview

SciSciNet Explorer provides an easy-to-use interface for accessing over 134 million scientific publications without requiring any API keys or technical expertise. Perfect for researchers, students, and anyone interested in exploring scientific literature.

## Features

### Main Search Interface
- Search for papers, authors, institutions, and research topics
- View detailed information including citations, authors, and abstracts
- Filter results by publication year, type, and more
- User-friendly card-based layout

### Paper Details & Analysis
- Detailed paper information and metadata
- Citation network visualization
- Citation timeline analysis
- Research topic/concept distribution charts
- Export individual papers as JSON or CSV

### Batch Search & Data Export
- Search and export up to 200 results at once
- Export data in multiple formats (CSV, Excel, JSON)
- Quick statistical analysis and visualizations
- Perfect for literature reviews and bibliometric studies

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download this repository:**
   ```bash
   git clone <repository-url>
   cd origin125
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser:**
   The application will automatically open in your default browser at `http://localhost:8501`

## Usage Guide

### 1. Basic Search

1. Open the application
2. Use the sidebar to select what you want to search (Papers, Authors, Institutions, or Concepts)
3. Enter your search term
4. Adjust filters as needed (for papers: year range, results per page)
5. View results in an easy-to-read card format

**Example searches:**
- Papers: "machine learning", "climate change", "quantum computing"
- Authors: "Albert Einstein", "Marie Curie"
- Institutions: "MIT", "Stanford University"
- Concepts: "artificial intelligence", "neuroscience"

### 2. Paper Details & Analysis

1. Navigate to the "Paper Details" page from the sidebar
2. Enter an OpenAlex Work ID or DOI
3. View comprehensive paper information including:
   - Full metadata and author information
   - Citation metrics and timeline
   - Citation network (papers citing this work)
   - Research topics/concepts
4. Export data in JSON or CSV format

**Finding Paper IDs:**
- Use the main search page to find papers
- Copy the OpenAlex ID or DOI from any paper
- Use DOIs from Google Scholar, PubMed, etc.

### 3. Batch Export

1. Navigate to the "Batch Export" page
2. Enter your search query
3. Select number of results (up to 200)
4. Apply filters if needed
5. Click "Search and Load Data"
6. View results in a spreadsheet-like format
7. Download in your preferred format:
   - **CSV**: For Excel, Google Sheets, or data analysis
   - **Excel**: Formatted spreadsheet
   - **JSON**: Complete raw data with all fields

## Project Structure

```
origin125/
├── app.py                      # Main application
├── sciscinet_api.py           # API wrapper for OpenAlex
├── pages/
│   ├── 1_Paper_Details.py    # Paper analysis page
│   └── 2_Batch_Export.py     # Batch search and export
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore file
└── README.md                 # This file
```

## Data Source

This application uses **OpenAlex**, an open catalog of scholarly papers, authors, institutions, and more. OpenAlex is:

- **Free and open**: No API key required
- **Comprehensive**: 134M+ publications
- **Up-to-date**: Regularly updated with new publications
- **Rich**: Includes citations, abstracts, author info, and more

Learn more: [https://openalex.org](https://openalex.org)

## Technical Details

### Technologies Used

- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis
- **Requests**: HTTP requests to OpenAlex API
- **OpenPyXL**: Excel file generation

### API Wrapper

The `sciscinet_api.py` module provides a simple Python interface to the OpenAlex API with methods for:

- Searching works (papers)
- Searching authors
- Searching institutions
- Searching concepts
- Getting citations
- Getting references

### Optional: Polite Pool

For faster API access, you can provide your email address:

1. Create a `.streamlit/secrets.toml` file:
   ```toml
   email = "your.email@example.com"
   ```

2. Restart the application

This enables OpenAlex's "polite pool" for faster response times.

## Use Cases

### For Researchers
- Literature reviews
- Finding related papers
- Tracking citations
- Identifying collaborators
- Exploring research trends

### For Students
- Finding papers for assignments
- Understanding research topics
- Tracking influential authors
- Learning about research institutions

### For Librarians
- Collection development
- Research support
- Bibliometric analysis
- Tracking institutional output

### For Data Scientists
- Bibliometric research
- Network analysis
- Citation pattern analysis
- Research trend prediction

## Troubleshooting

### Installation Issues

**Problem**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**: Make sure you've installed all requirements:
```bash
pip install -r requirements.txt
```

### Connection Issues

**Problem**: "Error loading data" or timeout errors

**Solution**:
- Check your internet connection
- Try again (OpenAlex API occasionally experiences high load)
- Reduce the number of results requested

### Search Returns No Results

**Solution**:
- Try different search terms
- Remove filters
- Use more general keywords
- Check spelling

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is open source and available for educational and research purposes.

## Acknowledgments

- **OpenAlex** for providing free access to scholarly data
- **SciSciNet** project at Northwestern University's Kellogg School
- **Streamlit** for the excellent web app framework

## Contact & Support

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review OpenAlex documentation: [https://docs.openalex.org](https://docs.openalex.org)
3. Open an issue in the repository

## Version

**Current Version**: 1.0.0

**Last Updated**: October 2025

---

Made with Python and Streamlit for easy scientific literature exploration
