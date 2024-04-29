import streamlit as st
from scripts.scraper import discover_links, setup_selenium_driver, scrape_urls
from scripts.embedding import generate_data_store
from scripts.inference import generate_response, init_db
from scripts.graphs import display_word_count_graph
from scripts.email_utils import send_phishing_email, generate_email_content


if 'responses' not in st.session_state:
    st.session_state['responses'] = []

with st.sidebar:
    st.title('RAG Embedding')
    base_url = st.text_input('Enter a URL to crawl', 'https://example.com')

    if st.button('Crawl', key='crawl_button'):
        with st.spinner('Crawling...'):
            discovered_urls = discover_links(base_url)
            st.session_state['discovered_urls'] = discovered_urls
            st.success(f"Discovered {len(discovered_urls)} URLs.")

    if 'discovered_urls' in st.session_state and st.session_state['discovered_urls']:
        selected_urls = {url: st.checkbox(url, key=f'checkbox_{url}', value=True) for url in st.session_state['discovered_urls']}
        selected_to_scrape = [url for url, selected in selected_urls.items() if selected]

        if st.button('Scrape selected URLs', key='scrape_selected_urls_button'):
            with st.spinner('Scraping...'):
                driver = setup_selenium_driver()
                scrape_urls(selected_to_scrape, driver)
                driver.quit()
                st.success('Done. Saved to /content')
                st.session_state['embeddings_ready'] = True

    if 'embeddings_ready' in st.session_state and st.session_state['embeddings_ready']:
        display_word_count_graph('./content')

    if 'embeddings_ready' in st.session_state and st.session_state['embeddings_ready']:
        model_name = st.selectbox('Select the embedding model', ['hkunlp/instructor-base', 'hkunlp/instructor-large', 'hkunlp/instructor-xl'], key='model_name_selectbox')

        if st.button('Generate embedding', key='generate_embedding_button'):
            with st.spinner('Generating embedding...'):
                generate_data_store(model_name)
                st.success('Embedding generated.')

st.title('RAG Inference')

model_name_for_inference = st.selectbox('Select the embedding model for inference', 
                          ['hkunlp/instructor-base', 'hkunlp/instructor-large', 'hkunlp/instructor-xl'], 
                          key='model_for_inference_selectbox')

if st.button('Load model', key='load_model_button'):
    with st.spinner('Initializing Embedding and ChromaDB...'):
        db = init_db(model_name_for_inference)
        st.session_state['db'] = db
        st.session_state['model_loaded'] = True
        st.success('Embedding and ChromaDB loaded successfully.')

if 'model_loaded' in st.session_state:
    use_embedding = st.checkbox('Use embedding', value=False, key='use_embedding_checkbox')
    question = st.text_input('Prompt', key='question_text_input')

    if st.button('Query', key='query_button'):
        with st.spinner('Generating response'):
            response = generate_response(question, st.session_state['db'], use_embedding=use_embedding)
            st.session_state['responses'].insert(0, {'question': question, 'response': response})

    if st.button('Send Phishing Email', key='send_phishing_email_button'):
        if st.session_state['responses']:
            last_response = st.session_state['responses'][0]['response']
            email_parts = generate_email_content(last_response)
            send_phishing_email(email_parts.get('Subject', 'No Subject'), email_parts.get('Body', 'No Body'))
            st.success("Phishing email sent successfully!")
        else:
            st.error("No response available to send.")

for entry in st.session_state.get('responses', []):
    st.write(f"Q: {entry['question']}")
    st.write(f"A: {entry['response']}")
    st.markdown("---")