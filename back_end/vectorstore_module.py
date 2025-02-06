from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


def create_embedding_model():
    """Updated HuggingFaceEmbeddings usage"""
    return HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-nli")

def create_vectorstore(splits, embedding_model):
    """분할된 문서(splits)를 FAISS 벡터스토어에 저장하고 반환한다."""
    vectordb = FAISS.from_documents(splits, embedding_model)
    return vectordb



class VectorStoreHandler:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        VectorStoreHandler 클래스는 주제 자료나 토론 과정을 텍스트로 받아서,
        이를 적절한 청크로 분할한 후 vectorstore(예: FAISS)로 저장하는 기능을 제공합니다.
        
        :param chunk_size: 텍스트 분할 시 청크 크기 (기본값: 500)
        :param chunk_overlap: 청크 간의 중복 길이 (기본값: 50)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # 기존 OpenAIEmbeddings 대신 HuggingFaceEmbeddings를 사용
        self.embeddings = create_embedding_model()
    
    def split_text(self, text: str) -> list:
        """
        입력된 텍스트를 지정한 청크 크기와 중복 길이에 따라 분할합니다.
        
        :param text: 분할할 원본 텍스트
        :return: 분할된 텍스트 청크들의 리스트
        """
        splitter = CharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        chunks = splitter.split_text(text)
        return chunks
    
    def store_topic_material(self, text: str) -> FAISS:
        """
        주제에 관한 자료(크롤링 등으로 수집한 텍스트)를 분할하여 FAISS vectorstore에 저장합니다.
        
        :param text: 주제 관련 원본 텍스트 자료
        :return: 생성된 FAISS 벡터 스토어 인스턴스
        """
        chunks = self.split_text(text)
        vectorstore = FAISS.from_texts(chunks, self.embeddings)
        print(f"주제 자료를 {len(chunks)}개의 청크로 분할하여 벡터 스토어에 저장했습니다.")
        return vectorstore