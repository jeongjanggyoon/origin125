"""
Paper Details and Citation Analysis Page
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sciscinet_api import SciSciNetAPI
import sys
import os

# Add parent directory to path to import sciscinet_api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Paper Details - SciSciNet Explorer",
    page_icon="📄",
    layout="wide"
)


@st.cache_resource
def get_api():
    """Initialize and cache the API instance"""
    email = st.secrets.get("email", None) if hasattr(st, 'secrets') else None
    return SciSciNetAPI(email=email)


def visualize_citation_network(work_id: str, api: SciSciNetAPI):
    """Create a citation network visualization"""
    st.subheader("Citation Network")

    with st.spinner("Loading citation data..."):
        # Get citations (papers that cite this work)
        citations = api.get_citations(work_id, per_page=50)
        citing_works = citations.get('results', [])

        # Get references (papers cited by this work)
        references = api.get_references(work_id)

        if not citing_works and not references:
            st.info("No citation data available for this paper.")
            return

        # Display metrics
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Papers Citing This Work", len(citing_works))

        with col2:
            st.metric("Papers Cited by This Work", len(references))

        # Show citing papers
        if citing_works:
            st.subheader("Recent Citations")

            # Create a dataframe for easy display
            citation_data = []
            for work in citing_works[:10]:  # Show top 10
                citation_data.append({
                    'Title': work.get('title', 'Untitled')[:100],
                    'Year': work.get('publication_year', 'N/A'),
                    'Citations': work.get('cited_by_count', 0),
                    'Authors': ', '.join([
                        auth.get('author', {}).get('display_name', 'Unknown')
                        for auth in work.get('authorships', [])[:3]
                    ])
                })

            df = pd.DataFrame(citation_data)
            st.dataframe(df, use_container_width=True)


def display_publication_timeline(work: dict, api: SciSciNetAPI):
    """Display citation timeline"""
    st.subheader("Citation Timeline")

    counts_by_year = work.get('counts_by_year', [])

    if not counts_by_year:
        st.info("No citation timeline data available.")
        return

    # Create dataframe
    df = pd.DataFrame(counts_by_year)

    if df.empty:
        st.info("No citation timeline data available.")
        return

    # Create line chart
    fig = px.line(
        df,
        x='year',
        y='cited_by_count',
        title='Citations Over Time',
        labels={'year': 'Year', 'cited_by_count': 'Number of Citations'}
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Citations",
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)


def display_concepts_chart(work: dict):
    """Display concept distribution"""
    st.subheader("Research Topics/Concepts")

    concepts = work.get('concepts', [])

    if not concepts:
        st.info("No concept data available.")
        return

    # Create dataframe
    concept_data = []
    for concept in concepts[:10]:  # Top 10 concepts
        concept_data.append({
            'Concept': concept.get('display_name', 'Unknown'),
            'Score': concept.get('score', 0),
            'Level': concept.get('level', 0)
        })

    df = pd.DataFrame(concept_data)

    # Create horizontal bar chart
    fig = px.bar(
        df,
        x='Score',
        y='Concept',
        orientation='h',
        title='Top Research Concepts',
        color='Level',
        color_continuous_scale='Blues'
    )

    fig.update_layout(
        xaxis_title="Relevance Score",
        yaxis_title="Concept",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)


def main():
    st.title("📄 Paper Details & Analysis")

    api = get_api()

    # Input for paper ID or DOI
    st.markdown("### Enter Paper Information")

    col1, col2 = st.columns([3, 1])

    with col1:
        paper_input = st.text_input(
            "Enter OpenAlex Work ID or DOI:",
            placeholder="e.g., W2741809807 or https://doi.org/10.1038/nature12373",
            help="You can enter either an OpenAlex Work ID (e.g., W2741809807) or a DOI"
        )

    with col2:
        search_button = st.button("Load Paper", type="primary")

    if search_button and paper_input:
        with st.spinner("Loading paper details..."):

            # Handle DOI input
            if 'doi.org' in paper_input or paper_input.startswith('10.'):
                # Search by DOI
                doi_clean = paper_input.split('doi.org/')[-1] if 'doi.org' in paper_input else paper_input
                search_results = api.search_works(f'doi:{doi_clean}', per_page=1)

                if search_results.get('results'):
                    work = search_results['results'][0]
                else:
                    st.error("Paper not found with the provided DOI.")
                    return
            else:
                # Get by OpenAlex ID
                work = api.get_work_by_id(paper_input)

                if 'error' in work:
                    st.error(f"Error loading paper: {work['error']}")
                    return

            # Display paper information
            st.markdown("---")

            # Title
            title = work.get('title', 'Untitled')
            st.markdown(f"## {title}")

            # Basic metrics
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

            with metric_col1:
                pub_year = work.get('publication_year', 'N/A')
                st.metric("Publication Year", pub_year)

            with metric_col2:
                citations = work.get('cited_by_count', 0)
                st.metric("Total Citations", f"{citations:,}")

            with metric_col3:
                ref_count = len(work.get('referenced_works', []))
                st.metric("References", ref_count)

            with metric_col4:
                is_oa = work.get('open_access', {}).get('is_oa', False)
                oa_status = "✓ Yes" if is_oa else "✗ No"
                st.metric("Open Access", oa_status)

            st.markdown("---")

            # Authors section
            st.subheader("Authors")
            authors = work.get('authorships', [])

            if authors:
                author_rows = []
                for auth in authors:
                    author_name = auth.get('author', {}).get('display_name', 'Unknown')
                    institutions = auth.get('institutions', [])
                    inst_names = ', '.join([inst.get('display_name', 'N/A') for inst in institutions])

                    author_rows.append({
                        'Name': author_name,
                        'Institutions': inst_names if inst_names else 'N/A'
                    })

                author_df = pd.DataFrame(author_rows)
                st.dataframe(author_df, use_container_width=True)

            # Publication info
            st.subheader("Publication Details")

            pub_col1, pub_col2 = st.columns(2)

            with pub_col1:
                pub_type = work.get('type', 'N/A').replace('-', ' ').title()
                st.write(f"**Type:** {pub_type}")

                host_venue = work.get('host_venue', {})
                if host_venue:
                    venue_name = host_venue.get('display_name', 'N/A')
                    st.write(f"**Venue:** {venue_name}")

            with pub_col2:
                doi = work.get('doi')
                if doi:
                    st.write(f"**DOI:** [{doi}]({doi})")

                openalex_id = work.get('id')
                if openalex_id:
                    st.write(f"**OpenAlex ID:** [{openalex_id}]({openalex_id})")

            # Abstract
            st.subheader("Abstract")
            abstract_inv = work.get('abstract_inverted_index', {})

            if abstract_inv:
                # Reconstruct abstract from inverted index
                abstract_words = {}
                for word, positions in abstract_inv.items():
                    for pos in positions:
                        abstract_words[pos] = word

                abstract = ' '.join([abstract_words[i] for i in sorted(abstract_words.keys())])
                st.write(abstract)
            else:
                st.info("Abstract not available.")

            st.markdown("---")

            # Visualizations
            tab1, tab2, tab3 = st.tabs(["Citation Network", "Citation Timeline", "Research Topics"])

            with tab1:
                visualize_citation_network(work.get('id', '').split('/')[-1], api)

            with tab2:
                display_publication_timeline(work, api)

            with tab3:
                display_concepts_chart(work)

            st.markdown("---")

            # Export options
            st.subheader("Export Data")

            export_col1, export_col2 = st.columns(2)

            with export_col1:
                # Export as JSON
                if st.button("Download as JSON"):
                    import json
                    json_data = json.dumps(work, indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=json_data,
                        file_name=f"paper_{work.get('id', 'unknown').split('/')[-1]}.json",
                        mime="application/json"
                    )

            with export_col2:
                # Export basic info as CSV
                if st.button("Download Basic Info as CSV"):
                    basic_info = {
                        'Title': [title],
                        'Year': [pub_year],
                        'Citations': [citations],
                        'Type': [pub_type],
                        'DOI': [doi if doi else 'N/A'],
                        'OpenAlex_ID': [openalex_id if openalex_id else 'N/A']
                    }
                    df = pd.DataFrame(basic_info)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"paper_{work.get('id', 'unknown').split('/')[-1]}.csv",
                        mime="text/csv"
                    )

    else:
        # Help information
        st.info("Enter an OpenAlex Work ID or DOI above to view detailed paper information and analysis.")

        st.markdown("### How to Find a Paper ID")
        st.markdown("""
        You can find papers in multiple ways:

        1. **Use the main search page** to search for papers and get their IDs
        2. **Visit OpenAlex.org** and search for a paper
        3. **Use a DOI** from any publication (e.g., from Google Scholar)

        **Example IDs:**
        - OpenAlex Work ID: `W2741809807`
        - DOI: `10.1038/nature12373`
        - Full DOI URL: `https://doi.org/10.1038/nature12373`
        """)


if __name__ == "__main__":
    main()
