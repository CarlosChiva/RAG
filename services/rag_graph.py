
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_nomic.embeddings import NomicEmbeddings
import sys
sys.path.append('../api-sindicato/')
from langchain.chains import RetrievalQA
from langchain import hub
from db.chroma_db import get_vectorstore_mock
QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt-llama")
import os
from langchain.prompts import PromptTemplate


### Add to vectorDB
vectorStore = get_vectorstore_mock("first")
retriever = vectorStore.as_retriever()
### LLm
local_llm = os.getenv("MODEL")
#---------------------------------------------------------------
### Router

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser


llm_router = ChatOllama(model=local_llm, format="json", temperature=0)

ROUTER_TEMPLATE= os.getenv("ROUTER_TEMPLATE")
prompt = PromptTemplate(
    template=ROUTER_TEMPLATE,
    input_variables=["question"],
)

question_router = prompt | llm_router | JsonOutputParser()

#Examples:
#question = "llm agent memory"
# docs = retriever.get_relevant_documents(question)
# doc_txt = docs[1].page_content
# print(question_router.invoke({"question": question}))


#------------------------------------------------------------------
### Retrieval Grader

from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser

# LLM
llm_retrieval_grader = ChatOllama(model=local_llm, format="json", temperature=0)
PROMT_RETRIEVAL_GRADER = os.getenv("PROMT_RETRIEVAL_GRADER")
retrieval_grader = prompt | llm_retrieval_grader | JsonOutputParser()

## Examples:
# question = "agent memory"
# docs = retriever.get_relevant_documents(question)
# doc_txt = docs[1].page_content
# print(retrieval_grader.invoke({"question": question, "document": doc_txt}))



#-----------------------------------------------------------------------------------
### Generate

from langchain import hub
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# Prompt
prompt = hub.pull("rlm/rag-prompt")

# LLM
llm_generate = ChatOllama(model=local_llm, temperature=0)


# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Chain
rag_chain = prompt | llm_generate | StrOutputParser()

# Run
# question = "agent memory"
# generation = rag_chain.invoke({"context": docs, "question": question})
# print(generation)

### Hallucination Grader

# LLM
llm_hallucination_grader = ChatOllama(model=local_llm, format="json", temperature=0)
HALLUCINATION_GRADER_PROMPT= os.getenv("HALLUCINATION_GRADER_PROMPT")
# Prompt
prompt = PromptTemplate(
    template=HALLUCINATION_GRADER_PROMPT,
    input_variables=["generation", "documents"],
)

hallucination_grader = prompt | llm_hallucination_grader | JsonOutputParser()
# hallucination_grader.invoke({"documents": docs, "generation": generation})


### Answer Grader

# LLM
llm_answer_grader = ChatOllama(model=local_llm, format="json", temperature=0)
ANSWER_GRADER_PROMPT= os.getenv("ANSWER_GRADER_PROMPT")
# Prompt
prompt = PromptTemplate(
    template=ANSWER_GRADER_PROMPT,
    input_variables=["generation", "question"],
)

answer_grader = prompt | llm_answer_grader | JsonOutputParser()

#Example
#answer_grader.invoke({"question": question, "generation": generation})

### Question Re-writer

# LLM
llm_question_rewriter = ChatOllama(model=local_llm, temperature=0.1)
QUESTION_REWRITER_PROMT= os.getenv("QUESTION_REWRITER_PROMPT")
# Prompt
re_write_prompt = PromptTemplate(
    template=QUESTION_REWRITER_PROMT,
    input_variables=["generation", "question"],
)

question_rewriter = re_write_prompt | llm_question_rewriter | StrOutputParser()

#Example
#question_rewriter.invoke({"question": question})



#-----------------------------------------------------------------------------------
# Graph Settings

from typing import List

from typing_extensions import TypedDict


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
    """

    question: str
    generation: str
    documents: List[str]
    context: str

#-----------------------------------------------------------------------------------
### Nodes

from langchain.schema import Document

def retrieve(state):
    """
    Retrieve documents

    Args:
        state (dict): The current graph state

    Returns:
        dict: New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")

    question = state["question"]



    vector_store= get_vectorstore_mock(collection_name="first")
    retrieval= vector_store.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm_retrieval_grader, retriever=retrieval, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    response=qa_chain.invoke({"query":question})
    doc_txt=response["result"]
    print("REsponse----------",response["result"])
    print("Output----------",{"documents": [doc_txt], "question": question})
    return {"documents": [doc_txt], "question": question}


def generate(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    print("Documents----------",documents[0])
    documents = documents[0]
    documents=documents.replace("\n","")
    
    # RAG generation
    generation = rag_chain.invoke({"context": documents, "question": question})
    return {"documents": documents, "question": question, "generation": generation}


def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with only filtered relevant documents
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    llm = ChatOllama(model=local_llm, format="json", temperature=0)

    prompt = PromptTemplate(
        template="""You are a grader assessing relevance of a retrieved document to a user question. \n 
        Here is the retrieved document: \n\n {document} \n\n
        Here is the user question: {question} \n
        If the document contains keywords related to the user question, grade it as relevant. \n
        It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
        Provide the binary score as a JSON with a single key 'score' and no premable or explanation.""",
        input_variables=["question", "document"],
    )
    retrieval_grader = prompt | llm | JsonOutputParser()
    
    question = state["question"]
    print("Question: ", question)
    # documents = state["documents"][0]
    # documents=documents.replace("\n","")
    # documents=dict(eval(documents))
    score=retrieval_grader.invoke({"question": question, "document": state["documents"]})
    print("Score:--------->",score)
    print("---------------------------")
    grade = score["score"]
    print("grade:--------->",grade)
    if grade == "yes":
        print("---GRADE: DOCUMENT RELEVANT---")
        return {"documents": state["documents"], "question": question}
    else:
        print("---GRADE: DOCUMENT NOT RELEVANT---")
        return {"documents": "", "question": question}


def transform_query(state):
    """
    Transform the query to produce a better question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates question key with a re-phrased question
    """

    print("---TRANSFORM QUERY---")
    question = state["question"]
    documents = state["documents"]

    # Re-write question
    better_question = question_rewriter.invoke({"question": question})
    return {"documents": documents, "question": better_question}


### Edges ###


def route_question(state):
    """
    Route question to web search or RAG.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """

    print("---ROUTE QUESTION---")
    question = state["question"]
    print(question)
    source={'datasource','vectorstore'}
    print("1",source)
    print("---ROUTE QUESTION TO RAG---")
    return "vectorstore"


def decide_to_generate(state):
    """
    Determines whether to generate an answer, or re-generate a question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """

    print("---ASSESS GRADED DOCUMENTS---")
    filtered_documents = state["documents"]
    print("Filtered documents: ", filtered_documents)
    if not filtered_documents:
        print("---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---")
        return "transform_query"
    else:
        print("---DECISION: GENERATE---")
        return "generate"


def grade_generation_v_documents_and_question(state):
    """
    Determines whether the generation is grounded in the document and answers question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Decision for next node to call
    """

    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]
    print(documents)
    print(generation)
    #score = hallucination_grader.invoke({"documents": documents, "generation": generation})
    score=hallucination_grader.invoke({"question": question, "generation": generation})
    print("score:--------->",score["answer"])
    grade = score["answer"]

    # Check hallucination
    if grade == "yes":
        return "useful"
    else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    
from langgraph.graph import END, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("retrieve", retrieve)  # retrieve documents
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("generate", generate)  # generate answer
workflow.add_node("transform_query", transform_query)  # transform query

# Build graph
workflow.add_conditional_edges(
    START,
    route_question,
    {
        "vectorstore": "retrieve",
    },
)

workflow.add_edge("retrieve", "grade_documents")  # route to next node to call

workflow.add_conditional_edges(
    "grade_documents",  # start node and its function -> grade_documents
    decide_to_generate,  # execute function to decide if answer is found
    {
        "transform_query": "transform_query",  # if answer is not found, route to next node
        "generate": "generate",  # if answer is found, route to next node
    },
)

workflow.add_edge("transform_query", "retrieve")  # add route between nodes

workflow.add_conditional_edges(
    "generate",  # node and its function called generate -> generate 
    grade_generation_v_documents_and_question,  # function to check if generation is grounded in documents and answers question
    {
        "useful": END,  # if generation is useful, end workflow
        "not useful": "transform_query",  # if generation is not useful, route to transform_query
    },
)

app = workflow.compile()


#-----------------------------------------------------------------------------------

#Example:
# from pprint import pprint

# # Run
# inputs = {"question": "What is the AlphaCodium paper about?"}
# for output in app.stream(inputs):
#     for key, value in output.items():
#         # Node
#         pprint(f"Node '{key}':")
#         # Optional: print full state at each node
#         # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
#     pprint("\n---\n")

# # Final generation
# pprint(value["generation"])

from pprint import pprint

# Run
# Run
question = {"question":"Cuando cita tengo?"}
response=""
for output in app.stream(question):
    for key, value in output.items():
        pass
    #     pprint(f"Node '{key}':")
    # print(output)
    pass
    response=output
print(output['generate']['generation'])    

