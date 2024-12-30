## RAG Project

This is my first project using AI, This project its a simple RAG that Use a vector database and fetching his collection the user can ask him any question about the information provided to system.
To Use this program, first you need get to installing ollama in your computer. to do it, use the next command in linux or visit the official web-page of ollama

---

**Architecture**
Tht architecture of this project its a simple program with a service backend and another for frontend
- Backen: it has all logical to process pdf documents (if need OCR algoritms or not) and use the communication with ollama models to embbed documents to chromaDB and use ollama's llm to use them to ask about the documentation keeped in collections of vector database.  Api made with FastApi framework

-  Frontend: A simple web service made with FastApi framework who has 2 windows, chat windows,and a windows to upload the documents and choice the collections where it will be added or create new collection with that 

---

> :memo: **Aviso**: There are some programs you shoud to have installing in your computer before to launch the project.

### Installing dependencies
The first dependecie you need to use this RAG's program is get ollama. For that, you can get it by his official web page.

<a href="https://ollama.com/download" target="_blank">Ollama web page</a>

If you are going to use it in linux you can use directly the next commands in your terminal:

#### Get Ollama service with the necesary models

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Download the models used in this project write the next commands:

```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
```
Once you get ollama service and get the necesary models you can download the project:

### Download project

Download the project with:
```bash
git clone  https://github.com/CarlosChiva/RAG.git
```

Go to main directory of project

```bash
cd ~/RAG/
```
#### Launch project

Inicialize the program using the next command:

```bash
docker compose up -d
```

To interact with program you find it in the next URL

http://localhost:5000

<a href="http://localhost:5000" target="_blank">Project launched</a>


![Image to Docker compose and llama](images/compose.png)

![descripción de la imagen](images/image.png)
