import sys
import json
import os
import io
import time

# API 키를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API 키 정보 로드

load_dotenv()
os.environ.get("OPENAI_API_KEY")

# 경로 추적을 위한 설정
os.environ["PWD"] = os.getcwd()

#출력의 인코딩을 utf-8로 설정한다
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# LangSmith 추적을 설정합니다. https://smith.langchain.com
from langchain_teddynote import logging

# 프로젝트 이름을 입력합니다.
logging.langsmith("RAG_REFER")


from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

# 시간 측정용
def check_time(input_text):
  end_time = time.time()

  print(f"{input_text}: {end_time - start_time} 초")
  
# 시간 측정용 코드
start_time = time.time()


# 벡터 스토어 경로
vectorstore_path = "vdb/faiss_vectorstore.pkl"

# 벡터 스토어 로드 또는 생성
if os.path.exists(vectorstore_path):
    # 기존 벡터 스토어 로드
    # vectorstore = FAISS.load_local(vectorstore_path, embeddings)

    # 단계 3: 임베딩(Embedding) 생성
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)

    # 시간 측정용 코드
    check_time("기존 벡터 스토어 로드")

else:
    # 단계 1: 문서 로드(Load Documents)
    loader = PDFPlumberLoader("data/SPRI_AI_Brief_2023년12월호_F.pdf")
    docs = loader.load()

    # 단계 2: 문서 분할(Split Documents)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    split_documents = text_splitter.split_documents(docs)

    # 벡터 스토어 생성
    vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)

    # 벡터 스토어 저장
    vectorstore.save_local(vectorstore_path)
    a = False # 출력 테스트


# 단계 5: 검색기(Retriever) 생성
# 문서에 포함되어 있는 정보를 검색하고 생성합니다.
retriever = vectorstore.as_retriever()

check_time("단계 5: 검색기(Retriever) 생성")

from langchain.chains import RetrievalQA

# 프롬프트 템플릿
template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer: """
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)


# 검색기와 언어 모델을 사용한 QA 체인 초기화
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-4o-mini", temperature=0),  # 언어 모델 설정
    chain_type="stuff",  # QA 체인 유형 설정
    retriever=retriever,  # 사전에 정의된 검색기 사용
    return_source_documents=True,  # 소스 문서 반환 설정
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}  # 프롬프트 템플릿 사용
)





if __name__ == "__main__":
  try:
    # query = "삼성전자가 만든 생성형 AI 이름은?"
    query = str(sys.argv[1])
    
    # result = qa_chain({"query": query})
    result = qa_chain.invoke({"query": query})
    answer = result['result']
    source_documents = result['source_documents']

    # print(json.dumps(f"answer : {a}"))
    # print(json.dumps(f"answer : {answer}, source_documents : {source_documents}"))
    print(json.dumps(f"answer : {answer}, source_documents : {source_documents}", ensure_ascii=False))
    check_time("출력완료")

  except ValueError:
    print("Error: Invalid arguments")
    sys.exit(1)