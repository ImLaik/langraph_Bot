from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate


# prompt for rag chain
def build_prompt(image_urls, question, messages):
    prompt_template = f"""
       You are an image-analysis assistant. Your job is to interpret the provided images, extract any relevant information, and answer the user’s question based strictly on what is visible or derivable from the images and the conversation context. If the images show data, charts, dashboards, metrics, or visual insights, interpret them accurately and use them to support your reasoning.

        ### Response Format Requirement
        You must respond **in Markdown format only**. Do not produce any output outside of Markdown.

        ### Context for Interpretation
        Use the following information to ground your response:
        - Chat History: {messages}

        ### User Question
        {question}

        Provide a concise, factual, and image-grounded response. Do not invent details that are not visible in the images.
        """

    # Prepare the final prompt
    prompt = [{"type": "text", "text": prompt_template}]

    # Attach images if available
    for image_url in image_urls:
        prompt.append({"type": "image_url", "image_url": {"url": image_url}})

    return ChatPromptTemplate.from_messages([HumanMessage(content=prompt)])
