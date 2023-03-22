import streamlit as st
import openai

# Set up OpenAI API client
openai.api_key = st.secrets["API_KEY"]


# function to get list of tasks
def generate_persona():
    st.session_state.flow = 1

    # Generate diverse persona

    persona = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"""You are a persona generator whose outputs favor ethnically,
             religiously, gendered, sexually, and demographically underrepresented individuals of various ages. 
             
             You favor also favor uncommon names when creating personas."""},
            {"role": "user", "content": f"""Create a persona for an individual with the following
            additional specific characteristics: {st.session_state.characteristics} and generate the output in
             the format of a persona description."""}
        ],
        temperature=0.9
    )

    st.session_state.persona_desc = persona.choices[0]['message']['content']

    persona_background = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"""You are a master storyteller and learning designer."""},
            {"role": "user", "content": f""" 
            
                    Here is a persona: {st.session_state.persona_desc}.

                    Using this persona, create a brief background story associated with the following 
                    context: {st.session_state.simulation_context}. This will be be used to 
                     introduce a learning simulation, DO NOT PROVIDE A CONCLUSION TO THE STORY. 

                     In developing this story, include the following four features of a compelling character:

                     1. The character should have a strong and defined dramatic need: what does the
                     character want to win, gain, obtain, or achieve?

                     2. They have an individual point of view: what makes the character's belief system
                      unique or different? 

                     3. They personify an attitude: how does the character act, hold themselves, and treat others?  

                     4. They go through some kind of change or transformation: what important changes have led the
                      character to where they are now facing the situation described previously?

                    """}
        ],
        temperature=0.8
    )

    st.session_state.persona_background_desc = persona_background.choices[0]['message']['content']

def return_to_generator():
    st.session_state.flow = 0


if 'flow' not in st.session_state or st.session_state.flow == 0:
    st.session_state.flow = 0

    st.title("Persona Generator	:snowflake:")

    st.markdown("### Greetings, let's create some diverse personas for case studies!")

    # Get user input
    st.session_state.characteristics = st.text_input("Any specific persona characteristics?",
                                                     "30-year-old, vegan, recently unemployed")
    st.session_state.simulation_context = st.text_input("What is the context of the simulation/case study?",
                                                        "recently entered therapy for depression")

    st.button("Get me a persona!", on_click=generate_persona, args="")

if st.session_state.flow == 1:
    st.write("Here is your persona:")
    st.markdown(st.session_state.persona_desc)
    st.text("-----------------")
    st.text("")
    st.write("Here is a background story for the persona, given the simulation context:")
    st.markdown(st.session_state.persona_background_desc)

    st.text("")
    st.text("")

    st.button("Roll the dice! (Give me another persona.) ", on_click=generate_persona, args="")
    st.button("Go back to persona generator.", on_click=return_to_generator, args="")
