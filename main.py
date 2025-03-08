import streamlit as st
from scrape import (
    scrapee,
    extractt,
    cleanup,
    split_dom_content,
)
from parse import parse_with_gemini  # Uncomment this line


st.title("AI WEB SCRAPPER")
url = st.text_input("Enter the URL")
if st.button("Scrape"):
    if not url:
        st.error("Please enter a valid URL.")
    else:
        try:
            st.write("Scraping...")
            result = scrapee(url)
            body_content = extractt(result)
            cleaned_content = cleanup(body_content)
            
            st.session_state.dom_content = cleaned_content
            with st.expander("View DOM content:"):
                st.text_area("DOM content", cleaned_content, height=300)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to extract from the DOM content:")
    
    if st.button("Parse Now"):
        if parse_description:
            st.write("Fetching the required content...")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            
            # Process with Gemini API and display results
            parsed_content = parse_with_gemini(dom_chunks, parse_description)
            
            # Display the results
            st.subheader("Extracted Content:")
            st.write(parsed_content)
