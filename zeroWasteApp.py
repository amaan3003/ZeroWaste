
# Zero-waste recipe suggester using local Dolphin LLM via Ollama
# Goal: take ingredients → prioritize expiring ones → ask LLM for creative zero-waste recipes

import streamlit as st                 
import ollama                          



st.set_page_config(page_title="Zero-Waste", page_icon="🍲")

st.title("ZERO WASTE RECIPIES 🍲")


with st.container(border=True):
    st.subheader("Input Ingredients")
    user_input = st.text_area(
        "What's in your kitchen? (with quantity)",
        placeholder="e.g., spinach:1, tomato:3",
        height=100
    )
    
    generateButton = st.button("🍳 Generate Recipes", use_container_width=True, type="primary")


if generateButton:
    with st.status("Dolphin is analyzing...", expanded=True) as status:
        st.write("Analyzing ingredients...")
        st.write("Contacting LLM...")
        status.update(label="Recipes Ready!", state="complete", expanded=False)


def parse_ingredients(input_str):
    
    if not input_str.strip():
        return [], []
 

    items = [item.strip() for item in input_str.split(",")]
    urgent = []
    normal = []
    
    for item in items:
        if ":" in item:
            try:
                name, days = item.split(":")
                urgent.append(f"{name} (expires in {days} days)")
            except:
                normal.append(item)
        else:
            normal.append(item)
            
    return urgent, normal

if generateButton:
    if not user_input.strip():
        st.warning("Pehle kuch ingredients toh likh lala!")
    else:
        # Ingredients parse karo
        urgent_list, normal_list = parse_ingredients(user_input)
        
        with st.status("Dolphin is cooking..", expanded=True) as status:
            st.write("Analyzing...")
            
            prompt = f"""
            You are a creative zero-waste chef. 
            URGENT (use these first): {', '.join(urgent_list)}
            STABLE ITEMS: {', '.join(normal_list)}
            Task: Give me 2 recipes using the URGENT items. 
            Format: Title, Ingredients (bold urgent ones), and Steps.
            """
        
            st.write("Contacting Local LLM...")
            try:
                response = ollama.chat(
                    model='dolphin3:8b', 
                    messages=[{'role': 'user', 'content': prompt}]
                )
                
                recipe_output = response['message']['content']
                status.update(label="Recipes Ready!", state="complete", expanded=False)
                
                st.markdown("---")
                st.markdown(recipe_output)
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Check the terminal if  'ollama serve' is running?")