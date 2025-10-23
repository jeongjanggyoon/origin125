"""
Batch Search and Data Export Page
"""

import streamlit as st
import pandas as pd
from sciscinet_api import SciSciNetAPI
import sys
import os
import json
from io import StringIO

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Batch Export - SciSciNet Explorer",
    page_icon="📊",
    layout="wide"
)


@st.cache_resource
def get_api():
    """Initialize and cache the API instance"""
    email = st.secrets.get("email", None) if hasattr(st, 'secrets') else None
    return SciSciNetAPI(email=email)


def convert_works_to_dataframe(works: list) -> pd.DataFrame:
    """Convert a list of works to a pandas DataFrame"""
    data = []

    for work in works:
        # Get authors
        authors = work.get('authorships', [])
        author_names = ', '.join([
            auth.get('author', {}).get('display_name', 'Unknown')
            for auth in authors[:5]
        ])

        # Get venue
        host_venue = work.get('host_venue', {})
        venue_name = host_venue.get('display_name', 'N/A')

        # Get first institution
        first_institution = 'N/A'
        if authors and authors[0].get('institutions'):
            first_institution = authors[0]['institutions'][0].get('display_name', 'N/A')

        data.append({
            'Title': work.get('title', 'Untitled'),
            'Authors': author_names,
            'Publication_Year': work.get('publication_year', 'N/A'),
            'Type': work.get('type', 'N/A'),
            'Venue': venue_name,
            'Citations': work.get('cited_by_count', 0),
            'Open_Access': work.get('open_access', {}).get('is_oa', False),
            'DOI': work.get('doi', 'N/A'),
            'OpenAlex_ID': work.get('id', 'N/A'),
            'First_Institution': first_institution
        })

    return pd.DataFrame(data)


def convert_authors_to_dataframe(authors: list) -> pd.DataFrame:
    """Convert a list of authors to a pandas DataFrame"""
    data = []

    for author in authors:
        affiliation = author.get('last_known_institution', {})
        inst_name = affiliation.get('display_name', 'N/A')

        data.append({
            'Name': author.get('display_name', 'Unknown'),
            'Works_Count': author.get('works_count', 0),
            'Cited_By_Count': author.get('cited_by_count', 0),
            'H_Index': author.get('summary_stats', {}).get('h_index', 0),
            'Institution': inst_name,
            'OpenAlex_ID': author.get('id', 'N/A')
        })

    return pd.DataFrame(data)


def main():
    st.title("📊 Batch Search & Data Export")

    api = get_api()

    st.markdown("""
    Use this page to search for multiple papers and export the results for further analysis.
    Perfect for literature reviews, bibliometric studies, and data collection.
    """)

    st.markdown("---")

    # Search configuration
    st.subheader("Configure Your Search")

    search_type = st.selectbox(
        "What do you want to search?",
        ["Papers", "Authors"]
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        search_query = st.text_input(
            "Search Query",
            placeholder="e.g., artificial intelligence in healthcare",
            help="Enter keywords, topics, or author names"
        )

    with col2:
        num_results = st.number_input(
            "Number of Results",
            min_value=10,
            max_value=200,
            value=50,
            step=10,
            help="Maximum 200 results per search"
        )

    # Additional filters for papers
    if search_type == "Papers":
        st.subheader("Advanced Filters")

        filter_col1, filter_col2, filter_col3 = st.columns(3)

        with filter_col1:
            use_year_filter = st.checkbox("Filter by Year")
            if use_year_filter:
                year_start = st.number_input("Start Year", min_value=1900, max_value=2025, value=2020)
                year_end = st.number_input("End Year", min_value=1900, max_value=2025, value=2024)

        with filter_col2:
            use_oa_filter = st.checkbox("Open Access Only")

        with filter_col3:
            use_type_filter = st.checkbox("Filter by Type")
            if use_type_filter:
                pub_type = st.selectbox(
                    "Publication Type",
                    ["article", "book", "book-chapter", "dataset", "dissertation", "preprint"]
                )

    # Search button
    if st.button("🔍 Search and Load Data", type="primary"):
        if not search_query:
            st.warning("Please enter a search query.")
        else:
            with st.spinner(f"Searching for {search_type.lower()}..."):

                if search_type == "Papers":
                    results = api.search_works(
                        query=search_query,
                        per_page=num_results
                    )

                    if 'error' in results:
                        st.error(f"Error: {results['error']}")
                    else:
                        works = results.get('results', [])
                        total_count = results.get('meta', {}).get('count', 0)

                        if works:
                            st.success(f"Found {total_count:,} papers (showing {len(works)})")

                            # Convert to DataFrame
                            df = convert_works_to_dataframe(works)

                            # Store in session state
                            st.session_state['search_results'] = df
                            st.session_state['search_results_raw'] = works
                            st.session_state['search_type'] = search_type
                        else:
                            st.warning("No results found. Try a different search term.")

                elif search_type == "Authors":
                    results = api.search_authors(
                        query=search_query,
                        per_page=num_results
                    )

                    if 'error' in results:
                        st.error(f"Error: {results['error']}")
                    else:
                        authors = results.get('results', [])
                        total_count = results.get('meta', {}).get('count', 0)

                        if authors:
                            st.success(f"Found {total_count:,} authors (showing {len(authors)})")

                            # Convert to DataFrame
                            df = convert_authors_to_dataframe(authors)

                            # Store in session state
                            st.session_state['search_results'] = df
                            st.session_state['search_results_raw'] = authors
                            st.session_state['search_type'] = search_type
                        else:
                            st.warning("No authors found. Try a different search term.")

    # Display results if available
    if 'search_results' in st.session_state:
        st.markdown("---")
        st.subheader("Search Results")

        df = st.session_state['search_results']

        # Display statistics
        if st.session_state['search_type'] == "Papers":
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

            with stat_col1:
                st.metric("Total Papers", len(df))

            with stat_col2:
                avg_citations = df['Citations'].mean()
                st.metric("Avg. Citations", f"{avg_citations:.1f}")

            with stat_col3:
                oa_count = df['Open_Access'].sum()
                st.metric("Open Access", f"{oa_count} ({oa_count/len(df)*100:.1f}%)")

            with stat_col4:
                year_range = f"{df['Publication_Year'].min()} - {df['Publication_Year'].max()}"
                st.metric("Year Range", year_range)

        elif st.session_state['search_type'] == "Authors":
            stat_col1, stat_col2, stat_col3 = st.columns(3)

            with stat_col1:
                st.metric("Total Authors", len(df))

            with stat_col2:
                avg_works = df['Works_Count'].mean()
                st.metric("Avg. Publications", f"{avg_works:.1f}")

            with stat_col3:
                avg_h_index = df['H_Index'].mean()
                st.metric("Avg. H-Index", f"{avg_h_index:.1f}")

        # Display the dataframe
        st.dataframe(df, use_container_width=True, height=400)

        st.markdown("---")

        # Export options
        st.subheader("📥 Export Data")

        export_col1, export_col2, export_col3 = st.columns(3)

        with export_col1:
            # CSV Export
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name=f"sciscinet_export_{st.session_state['search_type'].lower()}.csv",
                mime="text/csv",
                help="Download the data as a CSV file for Excel or other analysis tools"
            )

        with export_col2:
            # Excel Export
            # Convert to Excel
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Results')
            excel_data = output.getvalue()

            st.download_button(
                label="Download as Excel",
                data=excel_data,
                file_name=f"sciscinet_export_{st.session_state['search_type'].lower()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download as Excel file with formatting"
            )

        with export_col3:
            # JSON Export (full data)
            json_data = json.dumps(st.session_state['search_results_raw'], indent=2)
            st.download_button(
                label="Download as JSON (Full)",
                data=json_data,
                file_name=f"sciscinet_export_{st.session_state['search_type'].lower()}_full.json",
                mime="application/json",
                help="Download complete raw data in JSON format"
            )

        st.markdown("---")

        # Data summary
        st.subheader("📈 Quick Analysis")

        if st.session_state['search_type'] == "Papers":
            # Citations distribution
            st.markdown("#### Citation Distribution")
            import plotly.express as px

            fig = px.histogram(
                df,
                x='Citations',
                nbins=30,
                title='Distribution of Citations',
                labels={'Citations': 'Number of Citations', 'count': 'Number of Papers'}
            )
            st.plotly_chart(fig, use_container_width=True)

            # Publications by year
            st.markdown("#### Publications by Year")
            year_counts = df['Publication_Year'].value_counts().sort_index()
            fig2 = px.bar(
                x=year_counts.index,
                y=year_counts.values,
                labels={'x': 'Year', 'y': 'Number of Publications'},
                title='Publications Over Time'
            )
            st.plotly_chart(fig2, use_container_width=True)

        elif st.session_state['search_type'] == "Authors":
            # H-index distribution
            st.markdown("#### H-Index Distribution")
            import plotly.express as px

            fig = px.histogram(
                df,
                x='H_Index',
                nbins=30,
                title='Distribution of H-Index',
                labels={'H_Index': 'H-Index', 'count': 'Number of Authors'}
            )
            st.plotly_chart(fig, use_container_width=True)

    else:
        # Help section
        st.info("👆 Configure your search above and click 'Search and Load Data' to get started!")

        st.markdown("### 💡 Tips for Effective Searches")
        st.markdown("""
        - **Be specific**: Use detailed keywords for better results
        - **Use quotes**: Wrap exact phrases in quotes (e.g., "machine learning")
        - **Combine terms**: Use multiple keywords to narrow results
        - **Try variations**: Different phrasings can yield different results
        - **Export early**: Download your results before refining your search
        """)


# Add Excel support requirement
try:
    import openpyxl
except ImportError:
    st.sidebar.warning("Install openpyxl for Excel export: pip install openpyxl")


if __name__ == "__main__":
    main()
