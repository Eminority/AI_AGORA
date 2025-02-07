from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def create_embedding_model():
    """Updated HuggingFaceEmbeddings usage"""
    return HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-nli")

def create_vectorstore(splits, embedding_model):
    """분할된 문서(splits)를 FAISS 벡터스토어에 저장하고 반환한다."""
    vectordb = FAISS.from_documents(splits, embedding_model)
    return vectordb


#        :param chunk_size: 텍스트 분할 시 청크 크기 (기본값: 500)
#        :param chunk_overlap: 청크 간의 중복 길이 (기본값: 50)   
class VectorStoreHandler:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):


        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embeddings = create_embedding_model()
    
    def split_text(self, text: str) -> list:
        """
        텍스트를 일정한 크기로 분할합니다.
        
        :param text: 원본 텍스트 (문자열)
        :return: 분할된 텍스트 청크 리스트 (List[Document])
        """
        # ✅ CharacterTextSplitter 대신 RecursiveCharacterTextSplitter 사용 (더 안정적)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,  # 기본값 500
            chunk_overlap=self.chunk_overlap,  # 기본값 50
            length_function=len,
            separators=["\n\n", "\n", " ", ""],  # 구분자를 명확히 지정
        )
        
        # ✅ 문서를 분할하여 리스트로 반환
        chunks = splitter.split_text(text)
        
        # ✅ FAISS 벡터스토어에서 사용할 수 있도록 Document 객체로 변환
        from langchain.docstore.document import Document
        documents = [Document(page_content=chunk) for chunk in chunks]

        return documents

    #이후에 단순히 저장모듈로 사용해 다방면으로 활용할 수 있게 바꿀 계획

    def vectorstoring(self, texts: List[str]) -> FAISS:
        # 리스트의 각 요소를 개별적으로 분할한 후, 하나의 리스트로 합침
        chunks = []
        for text in texts:
            # self.split_text(text)가 Document 객체들의 리스트를 반환한다고 가정
            chunks.extend(self.split_text(text))
        
        # FAISS 벡터 스토어 생성 (Document 객체들을 사용하므로 from_documents 사용)
        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        
        print(f"총 {len(texts)}개의 문서를 받아 {len(chunks)}개의 청크로 분할하여 벡터 스토어에 저장했습니다.")
        return vectorstore