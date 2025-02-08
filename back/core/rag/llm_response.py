from together import Together
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Together client
client = Together(api_key="6b15da7f57fa038bfa3f954c088b2ed88f72ffeecc77502bb0c80d23784a3395")

def generate_llm_response(context, query):
    """Generate an LLM response using Together API."""
    prompt = (
        f"Answer the following question based on the provided context:\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        f"Answer:"
    )

    try:
        # Call the Together API
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",  # Replace with your model
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150  # Adjust max_tokens as needed
        )

        # Extract the response content
        answer = response.choices[0].message.content
        logger.info("LLM response generated successfully.")
        return answer
    except Exception as e:
        logger.error(f"Error generating LLM response: {e}")
        return "Sorry, an error occurred while generating the response."

# # Example usage
# context = "New York City is known for its iconic landmarks, vibrant culture, and diverse attractions."
# query = "What are some fun things to do in New York?"
# response = generate_llm_response(context, query)
# print(response)