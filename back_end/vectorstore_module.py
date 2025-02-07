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


#        :param chunk_size: 텍스트 분할 시 청크 크기 (기본값: 500)
#        :param chunk_overlap: 청크 간의 중복 길이 (기본값: 50)   
class VectorStoreHandler:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):


        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embeddings = create_embedding_model()
    
    def split_text(self, text: str) -> list:
        splitter = CharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        chunks = splitter.split_text(text)
        return chunks
    

    #이후에 단순히 저장모듈로 사용해 다방면으로 활용할 수 있게 바꿀 계획
    def vectorstoring_from_text(self, text: str) -> FAISS:
        """
        주제에 관한 자료(크롤링 등으로 수집한 텍스트)를 분할하여 FAISS vectorstore에 저장합니다.
        
        :param text: 주제 관련 원본 텍스트 자료
        :return: 생성된 FAISS 벡터 스토어 인스턴스
        """
        chunks = self.split_text(text)
        vectorstore = FAISS.from_texts(chunks, self.embeddings)
        print(f"주제 자료를 {len(chunks)}개의 청크로 분할하여 벡터 스토어에 저장했습니다.")
        return vectorstore