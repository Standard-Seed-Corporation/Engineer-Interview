# Interview Guide - Engineer Interview Challenge

## Welcome! 👋

Thank you for your interest in joining Standard Seed Corporation! This interview challenge is designed to assess your skills in:

- Working with GitHub Actions and CI/CD
- Building knowledge graphs from unstructured data
- Implementing RAG (Retrieval Augmented Generation) systems
- Using LangChain for AI applications
- Python programming and software engineering best practices

## What You'll Build

You'll be working with a collection of technical documents (currently provided as text files, but imagine they're PDFs) to build:

1. **A GitHub Actions Workflow** that automatically processes documents and creates a knowledge graph
2. **A RAG Chatbot** that can answer questions about the documents using LangChain

## Time Expectation

This challenge is designed to take approximately **5-7 hours** to complete:
- Task 1 (GitHub Actions + Knowledge Graph): 2-3 hours
- Task 2 (RAG Chatbot): 3-4 hours

Feel free to take breaks and work at your own pace. Quality matters more than speed!

## Getting Started

### Prerequisites

Before you begin, make sure you have:

- [ ] Python 3.8+ installed
- [ ] Git installed and configured
- [ ] A GitHub account
- [ ] An OpenAI API key (or access to another LLM provider)
- [ ] A code editor (VS Code, PyCharm, etc.)

### Setup Steps

1. **Fork this repository** to your own GitHub account

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Engineer-Interview.git
   cd Engineer-Interview
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

## Task 1: GitHub Actions Workflow

### Objective
Create a workflow that processes documents and builds a knowledge graph.

### What's Already Done
We've provided a **reference implementation** in `.github/workflows/organize_pdfs.yml`. 

### Your Task
Your task is to either:

**Option A**: Review, understand, and potentially improve the existing workflow
- Read through the workflow file
- Understand how it works
- Suggest or implement improvements
- Add more sophisticated entity extraction
- Improve the graph structure
- Add better visualizations

**Option B**: Create your own implementation from scratch
- Delete the existing workflow
- Design your own approach
- Implement it from scratch
- Make it better than the reference!

### What We're Looking For

✅ **Understanding**: Can you explain how the workflow works?

✅ **Code Quality**: Is the Python code clean, well-structured, and documented?

✅ **Error Handling**: Does it handle edge cases and errors gracefully?

✅ **Graph Quality**: Is the knowledge graph well-structured and meaningful?

✅ **Visualization**: Is the output useful and understandable?

✅ **Improvements**: Can you identify and implement improvements?

### Testing Your Workflow

1. Push changes to trigger the workflow:
   ```bash
   git add .github/workflows/organize_pdfs.yml
   git commit -m "Update workflow"
   git push
   ```

2. Check the Actions tab in your GitHub repository

3. Review the artifacts produced:
   - `knowledge_graph.json`
   - `knowledge_graph_visualization.png`

## Task 2: RAG Chatbot System

### Objective
Build a chatbot that can answer questions about the documents using RAG.

### What's Already Done
We've provided a **reference implementation** in the `chatbot/` directory.

### Your Task
Similar to Task 1, you can either:

**Option A**: Review, understand, and improve the existing implementation
- Read through the chatbot code
- Test it with different questions
- Identify limitations or bugs
- Implement improvements:
  - Better chunking strategies
  - Improved prompts
  - Additional features (e.g., source highlighting, confidence scores)
  - Better integration with the knowledge graph
  - Alternative LLM providers

**Option B**: Create your own implementation
- Design your own RAG architecture
- Use different libraries or approaches
- Implement from scratch
- Make it better!

### What We're Looking For

✅ **RAG Understanding**: Do you understand the RAG pattern?

✅ **LangChain Proficiency**: Can you effectively use LangChain?

✅ **Code Architecture**: Is the code well-organized and maintainable?

✅ **Response Quality**: Does the chatbot give accurate, helpful answers?

✅ **User Experience**: Is the interface intuitive and user-friendly?

✅ **Error Handling**: Does it handle edge cases gracefully?

✅ **Knowledge Graph Integration**: Does it leverage the knowledge graph effectively?

### Testing Your Chatbot

1. Make sure your `.env` file has valid API keys

2. Run the chatbot:
   ```bash
   python -m chatbot.rag_chatbot
   ```

3. Try asking questions like:
   - "What is machine learning?"
   - "Explain neural networks"
   - "What's the difference between supervised and unsupervised learning?"
   - "What Python libraries are used for data science?"

4. Test edge cases:
   - Questions about topics not in the documents
   - Follow-up questions
   - Ambiguous questions

## Evaluation Criteria

Your submission will be evaluated on:

### Technical Skills (40%)
- Code quality and organization
- Understanding of RAG concepts
- LangChain usage
- GitHub Actions knowledge
- Python proficiency

### Problem Solving (30%)
- Approach to the challenges
- Handling of edge cases
- Debugging and testing
- Performance optimization

### Communication (20%)
- Code documentation
- README clarity
- Comments where needed
- Explanation of design decisions

### Creativity (10%)
- Innovative solutions
- Additional features
- Improvements over the reference
- Unique approaches

## Submission Instructions

1. **Complete both tasks** in your forked repository

2. **Test everything** thoroughly:
   - Run the GitHub Actions workflow
   - Test the chatbot with various questions
   - Check for errors and edge cases

3. **Document your work**:
   - Update README.md if you made significant changes
   - Add comments explaining complex logic
   - Include a SOLUTION.md file with:
     - Overview of your approach
     - Design decisions and trade-offs
     - Challenges faced and how you solved them
     - Potential improvements for future work
     - How long you spent on each task

4. **Create a Pull Request**:
   - From your fork to this original repository
   - Title: "Interview Submission - [Your Name]"
   - Include a description summarizing your work

5. **Share your repository**:
   - Ensure it's public or grant us access
   - Include the PR link in your communication

## Tips for Success

💡 **Start Simple**: Get a basic version working first, then improve

💡 **Test Frequently**: Don't wait until the end to test your code

💡 **Read the Docs**: LangChain and other libraries have great documentation

💡 **Ask Questions**: If requirements are unclear, create an issue in the repository

💡 **Show Your Thinking**: Comments and documentation help us understand your approach

💡 **Have Fun**: This is a chance to learn and showcase your skills!

## Common Pitfalls to Avoid

❌ Overcomplicating the solution

❌ Not testing with the actual data

❌ Ignoring error handling

❌ Poor code organization

❌ Insufficient documentation

❌ Not managing API costs (use small models for testing!)

❌ Hardcoding values instead of using configuration

## Resources

### Documentation
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OpenAI API Documentation](https://platform.openai.com/docs/introduction)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [NetworkX Documentation](https://networkx.org/documentation/stable/)

### Tutorials
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [Building a RAG Chatbot](https://python.langchain.com/docs/use_cases/chatbots/)
- [GitHub Actions Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)

### Example Projects
- Look at other RAG implementations on GitHub
- Study LangChain example repositories
- Review knowledge graph projects

## Support

If you encounter issues:

1. Check the documentation
2. Review error messages carefully
3. Search for similar issues online
4. Create an issue in the repository (we'll respond!)
5. Don't hesitate to ask questions

## After Submission

After you submit, we'll:

1. Review your code (typically within 2-3 business days)
2. Test your implementation
3. Evaluate based on the criteria above
4. Schedule a technical discussion to talk about your solution

During the discussion, be prepared to:
- Explain your design decisions
- Walk through your code
- Discuss trade-offs you considered
- Talk about how you'd improve it with more time
- Answer questions about RAG and LangChain

## Final Notes

Remember, this challenge is designed to be realistic - you're not expected to build a perfect production system. We want to see:

- How you approach problems
- Your coding style and practices
- Your ability to learn new technologies
- How you handle requirements and constraints

**Most importantly**: We want to see your best work, but also respect your time. If you find yourself spending significantly more than the estimated time, that's okay - just document what you accomplished and what you'd do with more time.

Good luck! We're excited to see what you build! 🚀

---

**Questions?** Create an issue in the repository or reach out to us directly.
