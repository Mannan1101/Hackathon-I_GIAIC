# Quick Start: RAG Agent with OpenAI SDK

**Feature**: 003-rag-agent
**Purpose**: Guide for using the RAG agent to ask questions about book content
**Audience**: Developers who have completed spec-1 (ingestion) and spec-2 (retrieval validation)

---

## Prerequisites

Before using the RAG agent, ensure you have:

1. ✅ **Completed spec-1 (ingestion)**: Qdrant collection 'documentation' exists with embedded book chunks
2. ✅ **Completed spec-2 (retrieval validation)**: Verified retrieval pipeline works with `uv run python retrieve.main.py`
3. ✅ **OpenAI API Key**: Obtained from [OpenAI Platform](https://platform.openai.com/api-keys)
4. ✅ **Python 3.11+** and **UV package manager** installed

---

## Setup

### 1. Install OpenAI Package

```bash
cd backend
uv pip install openai
```

### 2. Add OpenAI API Key to .env

Open `backend/.env` and add your OpenAI API key:

```env
# Existing from spec-1/2
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_key
QDRANT_COLLECTION_NAME=documentation
COHERE_API_KEY=your_cohere_key
COHERE_MODEL=embed-english-v3.0

# NEW: Add this line
OPENAI_API_KEY=sk-proj-...your_openai_key_here
OPENAI_MODEL=gpt-3.5-turbo  # Optional, defaults to gpt-3.5-turbo
```

**Getting an OpenAI API Key**:
1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-` or `sk-`)
5. Paste into `.env` file

### 3. Verify Setup

Check that all required environment variables are set:

```bash
# From backend directory
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ OPENAI_API_KEY:', 'sk-...' + os.getenv('OPENAI_API_KEY', 'MISSING')[-10:])"
```

Expected output: `✅ OPENAI_API_KEY: sk-...xxxxxxxxxx`

---

## Usage

### Single Question Mode

Ask a single question and exit:

```bash
uv run python agent.py "What are the prerequisites?"
```

**Example Output**:
```
Question: What are the prerequisites?

[Retrieving information from documentation...]

Answer: According to Chapter 1: Getting Started, the prerequisites include:
- Python 3.11 or higher
- Git installed on your system
- Internet access to download dependencies

Additionally, from the Hardware Requirements section, you'll need:
- At least 4GB of RAM
- 10GB of free disk space

(Sources: Chapter 1: Getting Started, Resources: Hardware Requirements)
```

### Interactive Session Mode

Start an interactive conversation (multiple questions):

```bash
uv run python agent.py
```

**Example Interaction**:
```
RAG Agent - Ask questions about the book content
Type 'quit' or 'exit' to end the session

You: What are the prerequisites?
Agent: According to Chapter 1: Getting Started, the prerequisites include...

You: Tell me more about the hardware requirements
Agent: Based on the Resources: Hardware Requirements section, the system needs...

You: What comes after installation?
Agent: Following the installation chapter, the next section covers...

You: quit
Session ended. Asked 3 questions.
```

---

## Example Questions

### Good Questions (Relevant to Book Content)

These questions should retrieve relevant chunks and get answered:

1. **"What are the prerequisites?"** - Retrieves from Chapter 1 and Resources
2. **"How do I install the software?"** - Retrieves installation instructions
3. **"What hardware do I need?"** - Retrieves hardware requirements
4. **"Explain the setup process"** - Retrieves setup/configuration steps
5. **"What is Chapter 2 about?"** - Retrieves content from Chapter 2

### Follow-up Questions (Testing Multi-Turn Context)

These test the agent's ability to maintain conversation context:

1. First: **"What is Chapter 1 about?"** → Then: **"What comes next?"**
2. First: **"Tell me about prerequisites"** → Then: **"Tell me more about that"**
3. First: **"How do I install?"** → Then: **"What hardware do I need for that?"**

### Off-Topic Questions (Should Return "I don't have information")

These test that the agent doesn't hallucinate:

1. **"What is the weather today?"** - No weather info in book
2. **"How do I cook pasta?"** - No cooking info in book
3. **"What is quantum physics?"** - No physics info in book

**Expected Response**:
```
I don't have information about that in the book content. The documentation focuses on [actual book topics]. Is there something specific about the book you'd like to know?
```

---

## How It Works

1. **You ask a question** via command line or interactive mode
2. **Agent calls retrieval tool** (`retrieve_documentation`) to search Qdrant
3. **Retrieval tool queries Qdrant** using Cohere embeddings (reusing spec-2 pipeline)
4. **Tool returns relevant chunks** with metadata (page titles, sections, URLs)
5. **Agent generates answer** using ONLY the retrieved chunks
6. **Response includes citations** showing which chapters/sections were used

**Key Constraint**: The agent is instructed to use ONLY retrieved content. If no relevant information is found, it will say so instead of inventing answers.

---

## Interpreting Agent Responses

### Successful Answer with Citations

```
Answer: According to Chapter 2: Installation, you need to run the following command...

(Sources: Chapter 2: Installation, Resources: Software Setup)
```

**What this means**:
- ✅ Agent retrieved relevant chunks
- ✅ Answer is based on book content
- ✅ Citations provided for verification

### No Information Available

```
I don't have information about that in the book content. The documentation covers [topics], but not [your question topic].
```

**What this means**:
- ✅ Agent correctly identified off-topic question
- ✅ No hallucination occurred
- ✅ Agent suggested alternative approach

### Retrieval Error

```
I encountered an error retrieving information: Failed to connect to Qdrant (connection timeout). Please try again or check your Qdrant configuration.
```

**What this means**:
- ❌ Technical issue (Qdrant unavailable, network issue)
- ⚠️ Check Qdrant connection with: `uv run python retrieve.main.py`
- ⚠️ Verify QDRANT_URL and QDRANT_API_KEY in .env

---

## Troubleshooting

### Error: "Missing required environment variable: OPENAI_API_KEY"

**Cause**: OPENAI_API_KEY not set in .env file

**Solution**:
1. Open `backend/.env`
2. Add line: `OPENAI_API_KEY=sk-your_key_here`
3. Restart agent

### Error: "openai module not found"

**Cause**: OpenAI package not installed

**Solution**:
```bash
cd backend
uv pip install openai
```

### Error: "Incorrect API key provided"

**Cause**: Invalid or expired OpenAI API key

**Solution**:
1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new key
3. Update `.env` with new key
4. Verify key starts with `sk-`

### Error: "Rate limit exceeded"

**Cause**: Too many API requests to OpenAI in short time

**Solution**:
1. Wait 60 seconds and try again
2. Reduce question frequency
3. Consider upgrading OpenAI plan for higher rate limits
4. Check [usage dashboard](https://platform.openai.com/usage) for quota

### Error: "Collection 'documentation' does not exist"

**Cause**: Spec-1 ingestion not completed

**Solution**:
1. Run ingestion: `uv run python main.py`
2. Verify with: `uv run python retrieve.main.py`
3. Then try agent again

### Agent Gives Generic Answers (Not Using Book Content)

**Symptom**: Answers don't include citations or seem too general

**Cause**: Agent not calling retrieval tool properly

**Debug Steps**:
1. Check agent.py logs for tool call messages
2. Verify retrieval tool is defined in agent configuration
3. Test retrieval directly: `uv run python retrieve.main.py`
4. Review system prompt enforces "ALWAYS call tool"

### Agent Says "I don't have information" for Valid Questions

**Symptom**: Agent refuses to answer questions that should have content

**Cause**: No relevant chunks retrieved (low similarity scores)

**Debug Steps**:
1. Test same question with: `uv run python retrieve.main.py`
2. Check similarity scores (should be >0.5 for relevant content)
3. Verify Qdrant collection has data (check vector count)
4. Try rephrasing question more specifically

---

## Performance Expectations

Based on success criteria from spec.md:

| Metric | Target | How to Verify |
|--------|--------|---------------|
| **Response Time** | <5 seconds per question | Time from question to answer |
| **Answer Accuracy** | 80%+ correct answers (8 of 10) | Test with 10 questions from book topics |
| **Citation Rate** | 90%+ of answers include sources | Count citations in 20 answers |
| **Off-Topic Handling** | 100% graceful responses | Ask 5 unrelated questions, verify no hallucination |
| **Multi-Turn Context** | 10+ turns coherent | Conduct 15-turn conversation, verify relevance |

**Testing**:
1. Ask 10 questions about book content → verify 8+ answered correctly
2. Ask 5 off-topic questions → verify all return "I don't have information"
3. Conduct 5-turn conversation with follow-ups → verify context maintained

---

## Configuration Options

### Changing the OpenAI Model

Edit `.env` to use a different model:

```env
OPENAI_MODEL=gpt-4-turbo  # More capable but slower/expensive
# OR
OPENAI_MODEL=gpt-3.5-turbo  # Faster and cheaper (default)
```

**Model Tradeoffs**:
- **gpt-3.5-turbo**: Faster, cheaper, good for most questions
- **gpt-4-turbo**: Better reasoning, more accurate, but 10x cost

### Adjusting Retrieval Parameters

In interactive mode, you can modify retrieval behavior by editing `agent.py`:

```python
# Retrieve more chunks for complex questions
top_k = 10  # Default: 5

# Set minimum similarity threshold
similarity_threshold = 0.5  # Default: 0.0 (return all results)
```

**When to increase top_k**:
- Complex questions requiring multiple sources
- Synthesis questions ("How do these relate?")
- Multi-step processes

**When to set similarity_threshold**:
- Reduce noise from low-relevance chunks
- Improve precision at cost of recall
- Typical values: 0.5-0.7

---

## Next Steps

After successfully using the agent:

1. **Test all success criteria** (see spec.md SC-001 to SC-007)
2. **Customize system prompt** for specific use cases (edit agent.py)
3. **Experiment with questions** to understand retrieval quality
4. **Monitor OpenAI usage** at [usage dashboard](https://platform.openai.com/usage)
5. **Integrate into larger application** (if needed, outside spec-3 scope)

---

## Limitations & Known Issues

**Current Limitations** (per spec out-of-scope):

- ❌ **No persistent sessions**: Conversation lost when agent exits
- ❌ **No streaming responses**: Full response returned at once
- ❌ **No multi-user support**: One conversation at a time
- ❌ **No web UI**: Command-line only
- ❌ **No authentication**: Anyone with access can run agent
- ❌ **No caching**: Every question triggers new retrieval + LLM call

**Workarounds**:
- For persistence: Save conversation to file manually
- For streaming: Future enhancement (requires async implementation)
- For web UI: Integrate with FastAPI (future spec)

**Context Window Limits**:
- Conversations grow in memory (messages array)
- Typical limit: ~20 turns before context too large
- Solution: Restart agent.py for fresh session

---

## Example Session Transcript

```bash
$ uv run python agent.py

RAG Agent - Ask questions about the book content
Type 'quit' or 'exit' to end the session

You: What are the prerequisites?
[Retrieving information from documentation...]
Agent: According to Chapter 1: Getting Started, the prerequisites include:
- Python 3.11 or higher
- Git installed on your system
- Internet access to download dependencies

Additionally, from the Hardware Requirements section:
- At least 4GB of RAM
- 10GB of free disk space

(Sources: Chapter 1: Getting Started, Resources: Hardware Requirements)

You: How do I install it?
[Retrieving information from documentation...]
Agent: Based on Chapter 2: Installation, the installation process is:

1. Clone the repository: git clone <repo-url>
2. Navigate to the project directory
3. Run the setup script: ./setup.sh
4. Verify installation: python --version

(Source: Chapter 2: Installation)

You: What is quantum physics?
[Retrieving information from documentation...]
Agent: I don't have information about quantum physics in the book content. The documentation focuses on software installation, prerequisites, and hardware requirements. Is there something specific about the book topics you'd like to know?

You: quit
Session ended. Asked 3 questions. Thank you!
```

---

## Support & Feedback

For issues with:
- **Ingestion or retrieval**: See `specs/001-doc-rag-ingestion/quickstart.md` and `specs/002-rag-retrieval-validation/quickstart.md`
- **Agent behavior**: Review system prompt in `agent.py`
- **OpenAI API**: Check [OpenAI documentation](https://platform.openai.com/docs)
- **Qdrant**: Check [Qdrant documentation](https://qdrant.tech/documentation/)
