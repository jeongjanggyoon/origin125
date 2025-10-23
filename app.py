"""
SciSciNet Explorer - User-Friendly GUI
A simple interface to explore scientific publications using SciSciNet/OpenAlex data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sciscinet_api import SciSciNetAPI
from datetime import datetime
import json


# Page configuration
st.set_page_config(
    page_title="SciSciNet Explorer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .paper-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #1f77b4;
    }
    .metric-card {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_api():
    """Initialize and cache the API instance"""
    email = st.secrets.get("email", None) if hasattr(st, 'secrets') else None
    return SciSciNetAPI(email=email)


def display_work_card(work: dict, show_abstract: bool = False):
    """Display a single work/paper in a card format"""
    with st.container():
        st.markdown('<div class="paper-card">', unsafe_allow_html=True)

        # Title
        title = work.get('title', 'Untitled')
        st.markdown(f"### {title}")

        # Authors
        authors = work.get('authorships', [])
        if authors:
            author_names = [auth.get('author', {}).get('display_name', 'Unknown')
                            for auth in authors[:5]]
            if len(authors) > 5:
                author_names.append(f"... and {len(authors) - 5} more")
            st.markdown(f"**Authors:** {', '.join(author_names)}")

        # Publication info
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            pub_year = work.get('publication_year', 'N/A')
            st.metric("Year", pub_year)

        with col2:
            cited_by = work.get('cited_by_count', 0)
            st.metric("Citations", cited_by)

        with col3:
            pub_type = work.get('type', 'N/A').replace('-', ' ').title()
            st.metric("Type", pub_type)

        with col4:
            is_oa = work.get('open_access', {}).get('is_oa', False)
            oa_status = "Yes" if is_oa else "No"
            st.metric("Open Access", oa_status)

        # Abstract
        if show_abstract:
            abstract_inv = work.get('abstract_inverted_index', {})
            if abstract_inv:
                # Reconstruct abstract from inverted index
                abstract_words = {}
                for word, positions in abstract_inv.items():
                    for pos in positions:
                        abstract_words[pos] = word

                abstract = ' '.join([abstract_words[i] for i in sorted(abstract_words.keys())])
                with st.expander("Show Abstract"):
                    st.write(abstract)

        # Links
        doi = work.get('doi')
        openalex_id = work.get('id')

        link_cols = st.columns([1, 1, 1, 3])
        with link_cols[0]:
            if doi:
                st.markdown(f"[DOI Link]({doi})")
        with link_cols[1]:
            if openalex_id:
                st.markdown(f"[OpenAlex]({openalex_id})")
        with link_cols[2]:
            # Add a button to view details
            if st.button("View Details", key=f"details_{work.get('id', '')}"):
                st.session_state['selected_work'] = work

        st.markdown('</div>', unsafe_allow_html=True)


def main():
    """Main application function"""

    # Header
    st.markdown('<p class="main-header">📚 SciSciNet Explorer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Explore 134M+ Scientific Publications with Ease</p>',
                unsafe_allow_html=True)

    # Initialize API
    api = get_api()

    # Sidebar
    with st.sidebar:
        st.header("🔍 Search Options")

        search_type = st.selectbox(
            "What do you want to search?",
            ["Papers", "Authors", "Institutions", "Concepts/Topics"]
        )

        search_query = st.text_input(
            "Enter your search term:",
            placeholder="e.g., machine learning, climate change"
        )

        # Advanced filters for papers
        if search_type == "Papers":
            st.subheader("Filters")

            year_range = st.slider(
                "Publication Year Range",
                1900,
                datetime.now().year,
                (2010, datetime.now().year)
            )

            per_page = st.slider(
                "Results per page",
                10, 100, 25, 5
            )

            show_abstracts = st.checkbox("Show abstracts", value=False)

        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This tool provides easy access to **SciSciNet**, a massive database of
        scientific publications built on OpenAlex data.

        **Features:**
        - Search papers, authors, and institutions
        - View citation metrics
        - Explore citation networks
        - Export data for analysis
        """)

    # Main content area
    if search_query:
        with st.spinner(f"Searching for {search_type.lower()}..."):

            if search_type == "Papers":
                results = api.search_works(
                    query=search_query,
                    page=1,
                    per_page=per_page
                )

                if 'error' in results:
                    st.error(f"Error: {results['error']}")
                else:
                    works = results.get('results', [])
                    total_count = results.get('meta', {}).get('count', 0)

                    if works:
                        st.success(f"Found {total_count:,} papers")

                        # Display results
                        for work in works:
                            display_work_card(work, show_abstract=show_abstracts)

                    else:
                        st.warning("No results found. Try a different search term.")

            elif search_type == "Authors":
                results = api.search_authors(query=search_query, per_page=25)

                if 'error' in results:
                    st.error(f"Error: {results['error']}")
                else:
                    authors = results.get('results', [])
                    total_count = results.get('meta', {}).get('count', 0)

                    if authors:
                        st.success(f"Found {total_count:,} authors")

                        for author in authors:
                            with st.container():
                                st.markdown('<div class="paper-card">', unsafe_allow_html=True)

                                name = author.get('display_name', 'Unknown')
                                st.markdown(f"### {name}")

                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    works_count = author.get('works_count', 0)
                                    st.metric("Publications", works_count)

                                with col2:
                                    cited_by = author.get('cited_by_count', 0)
                                    st.metric("Total Citations", cited_by)

                                with col3:
                                    h_index = author.get('summary_stats', {}).get('h_index', 0)
                                    st.metric("H-Index", h_index)

                                # Institution
                                affiliation = author.get('last_known_institution', {})
                                if affiliation:
                                    inst_name = affiliation.get('display_name', 'Unknown')
                                    st.markdown(f"**Affiliation:** {inst_name}")

                                # OpenAlex link
                                author_id = author.get('id')
                                if author_id:
                                    st.markdown(f"[View on OpenAlex]({author_id})")

                                st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning("No authors found. Try a different search term.")

            elif search_type == "Institutions":
                results = api.search_institutions(query=search_query, per_page=25)

                if 'error' in results:
                    st.error(f"Error: {results['error']}")
                else:
                    institutions = results.get('results', [])
                    total_count = results.get('meta', {}).get('count', 0)

                    if institutions:
                        st.success(f"Found {total_count:,} institutions")

                        for inst in institutions:
                            with st.container():
                                st.markdown('<div class="paper-card">', unsafe_allow_html=True)

                                name = inst.get('display_name', 'Unknown')
                                st.markdown(f"### {name}")

                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    works_count = inst.get('works_count', 0)
                                    st.metric("Publications", works_count)

                                with col2:
                                    cited_by = inst.get('cited_by_count', 0)
                                    st.metric("Total Citations", cited_by)

                                with col3:
                                    country = inst.get('country_code', 'N/A')
                                    st.metric("Country", country)

                                # Type and homepage
                                inst_type = inst.get('type', 'N/A')
                                st.markdown(f"**Type:** {inst_type}")

                                homepage = inst.get('homepage_url')
                                inst_id = inst.get('id')

                                link_col1, link_col2 = st.columns(2)
                                with link_col1:
                                    if homepage:
                                        st.markdown(f"[Website]({homepage})")
                                with link_col2:
                                    if inst_id:
                                        st.markdown(f"[OpenAlex]({inst_id})")

                                st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning("No institutions found. Try a different search term.")

            elif search_type == "Concepts/Topics":
                results = api.search_concepts(query=search_query, per_page=25)

                if 'error' in results:
                    st.error(f"Error: {results['error']}")
                else:
                    concepts = results.get('results', [])
                    total_count = results.get('meta', {}).get('count', 0)

                    if concepts:
                        st.success(f"Found {total_count:,} concepts")

                        for concept in concepts:
                            with st.container():
                                st.markdown('<div class="paper-card">', unsafe_allow_html=True)

                                name = concept.get('display_name', 'Unknown')
                                st.markdown(f"### {name}")

                                description = concept.get('description')
                                if description:
                                    st.markdown(f"*{description}*")

                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    works_count = concept.get('works_count', 0)
                                    st.metric("Related Papers", works_count)

                                with col2:
                                    cited_by = concept.get('cited_by_count', 0)
                                    st.metric("Total Citations", cited_by)

                                with col3:
                                    level = concept.get('level', 0)
                                    st.metric("Hierarchy Level", level)

                                # Wikidata link
                                wikidata = concept.get('wikidata')
                                concept_id = concept.get('id')

                                link_col1, link_col2 = st.columns(2)
                                with link_col1:
                                    if wikidata:
                                        st.markdown(f"[Wikidata]({wikidata})")
                                with link_col2:
                                    if concept_id:
                                        st.markdown(f"[OpenAlex]({concept_id})")

                                st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning("No concepts found. Try a different search term.")

    else:
        # Welcome screen
        st.info("👈 Use the sidebar to start searching!")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🎯 What can you do?")
            st.markdown("""
            - **Search Papers**: Find scientific publications by title, keywords, or topics
            - **Explore Authors**: Discover researchers and their work
            - **Find Institutions**: Search universities and research organizations
            - **Browse Topics**: Explore scientific concepts and fields
            """)

        with col2:
            st.markdown("### 📊 Data Source")
            st.markdown("""
            This application uses **OpenAlex**, an open catalog of scholarly papers,
            authors, institutions, and more. OpenAlex powers SciSciNet, providing
            access to over 134 million publications.

            **No API key required!** Just start searching.
            """)

        st.markdown("---")
        st.markdown("### 🚀 Quick Start Examples")

        example_col1, example_col2, example_col3 = st.columns(3)

        with example_col1:
            if st.button("Search: Machine Learning"):
                st.session_state['example_search'] = "machine learning"
                st.rerun()

        with example_col2:
            if st.button("Search: Climate Change"):
                st.session_state['example_search'] = "climate change"
                st.rerun()

        with example_col3:
            if st.button("Search: Quantum Computing"):
                st.session_state['example_search'] = "quantum computing"
                st.rerun()


if __name__ == "__main__":
    main()
