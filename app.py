import gradio as gr
import os
import sys
import warnings
from pathlib import Path
from datetime import datetime
import subprocess
import tempfile

# Ignore pysbd SyntaxWarning
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Add the project directory to the path to import the blog_writer module
sys.path.append(str(Path(__file__).parent))

# Import the BlogWriter crew    
from src.blog_writer.crew import BlogWriter

def generate_blog(topic):
    """
    Generate a blog post on the given topic using the blog writer crew.
    
    Args:
        topic (str): The topic for the blog post
    
    Returns:
        str: The generated blog post in markdown format
    """
    try:
        print(f"\n=== Generating blog post about: {topic} ===\n")
        
        # Prepare inputs with topic and current date
        inputs = {
            'topic': topic,
            "current_date": str(datetime.now())
        }

        # Create and run the crew
        result = BlogWriter().crew().kickoff(inputs=inputs)
        
        # Check for report.md file first
        report_path = Path('report.md')
        if report_path.exists():
            with open(report_path, 'r') as f:
                blog_content = f.read()
                # Clean up the markdown syntax if needed
                if blog_content.startswith("```markdown"):
                    blog_content = blog_content.replace("```markdown", "", 1)
                if blog_content.endswith("```"):
                    blog_content = blog_content[:-3]
                return blog_content
        
        # If no report.md, use the result directly
        if hasattr(result, 'raw'):
            return result.raw
        else:
            return result
            
    except Exception as e:
        return f"An error occurred while generating the blog: {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="AI Blog Writer") as demo:
    gr.Markdown("# AI Blog Writer")
    gr.Markdown("Enter a topic and let our AI agents create a professional blog post for you!")
    
    with gr.Row():
        with gr.Column():
            topic_input = gr.Textbox(
                label="Blog Topic",
                placeholder="Enter the topic for your blog post (e.g., 'The Evolution of AI', 'Remote Work Trends', etc.)",
                lines=2
            )
            generate_button = gr.Button("Generate Blog Post", variant="primary")
        
    with gr.Row():
        with gr.Column():
            output = gr.Markdown(label="Generated Blog Post")
    
    # Set up the button click event
    generate_button.click(
        fn=generate_blog,
        inputs=[topic_input],
        outputs=[output],
        api_name="generate"
    )
    
    gr.Markdown("## How it works")
    gr.Markdown("""
    This application uses a team of AI agents to create your blog post:
    
    1. **Planner**: Researches the topic and creates an outline
    2. **Writer**: Drafts the complete blog post based on the plan
    3. **Editor**: Reviews and improves the content
    4. **Reviewer**: Performs a final quality check
    
    The process may take a few minutes depending on the complexity of your topic.
    """)

if __name__ == "__main__":
    demo.launch()