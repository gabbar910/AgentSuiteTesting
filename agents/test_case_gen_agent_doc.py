import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from fastapi import UploadFile, HTTPException
import io

# Load environment variables
load_dotenv()

class TestCaseGenDocAgentWrapper:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        
        self.prompt_template = """
You are a test case generation specialist. I will provide you with a document containing requirements, specifications, or user stories, and you will generate comprehensive test cases covering frontend, backend, and integration scenarios.

### Instructions
1. Analyze the provided document content thoroughly
2. Extract all testable requirements and user stories
3. Identify all testable scenarios including:
    - Happy path scenarios
    - Edge cases and boundary conditions
    - Error handling scenarios
    - Integration points
    - Business logic validation
4. Generate test cases in the following format for each scenario:
    - Test Case ID (TC001, TC002, etc.)
    - Test Case Title
    - Test Category (Frontend/Backend/Integration/API/Database)
    - Priority (High/Medium/Low)
    - Preconditions
    - Test Steps (numbered and detailed)
    - Expected Results
    - Test Data Requirements
    - Post-conditions
5. Cover the following types of testing:
    - Functional Testing
    - UI/UX Testing
    - API Testing
    - Database Testing
    - Integration Testing
    - Negative Testing
    - Security Testing (if applicable)
    - Performance Testing (if applicable)
6. Ensure test cases are clear, actionable, and cover all acceptance criteria mentioned in the document
7. Group related test cases by feature or module
8. Include traceability back to specific requirements in the document

### Document Content:
{document_content}
"""

    def extract_text_from_pdf(self, file: UploadFile) -> str:
        """Extract text content from uploaded PDF file"""
        try:
            # Read the file content
            file_content = file.file.read()
            
            # Reset file pointer for potential future reads
            file.file.seek(0)
            
            # Open PDF with PyMuPDF
            pdf_document = fitz.open(stream=file_content, filetype="pdf")
            
            extracted_text = ""
            
            # Extract text from each page
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                page_text = page.get_text()
                extracted_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            
            pdf_document.close()
            
            if not extracted_text.strip():
                raise HTTPException(status_code=400, detail="No text content found in the PDF")
            
            return extracted_text
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing PDF: {str(e)}")

    def validate_pdf_file(self, file: UploadFile) -> None:
        """Validate the uploaded file"""
        # Check file type
        if not file.content_type == "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Check file size (max 20MB)
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        max_size = 20 * 1024 * 1024  # 20MB
        if file_size > max_size:
            raise HTTPException(status_code=400, detail="File size exceeds 20MB limit")
        
        # Check if file is empty
        if file_size == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")

    def chunk_text(self, text: str, max_chunk_size: int = 8000) -> list:
        """Split large text into manageable chunks for processing"""
        if len(text) <= max_chunk_size:
            return [text]
        
        chunks = []
        words = text.split()
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1  # +1 for space
            if current_size + word_size > max_chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks

    def process_pdf(self, file: UploadFile, test_category: str = "All", priority_filter: str = "All") -> str:
        """Process PDF file and generate test cases"""
        try:
            # Validate the file
            self.validate_pdf_file(file)
            
            # Extract text from PDF
            document_text = self.extract_text_from_pdf(file)
            
            # Add filtering instructions to prompt if specified
            filter_instructions = ""
            if test_category != "All":
                filter_instructions += f"\nFocus primarily on {test_category} test cases."
            if priority_filter != "All":
                filter_instructions += f"\nPrioritize {priority_filter} priority test cases."
            
            # Check if text is too large and needs chunking
            chunks = self.chunk_text(document_text)
            
            if len(chunks) == 1:
                # Process single chunk
                prompt = self.prompt_template.format(document_content=document_text) + filter_instructions
                result = self.llm.invoke(prompt)
                return result.content if hasattr(result, 'content') else str(result)
            else:
                # Process multiple chunks and combine results
                all_results = []
                for i, chunk in enumerate(chunks):
                    chunk_prompt = self.prompt_template.format(document_content=chunk) + filter_instructions
                    chunk_prompt += f"\n\nNote: This is part {i+1} of {len(chunks)} of the document. Generate test cases for this section and ensure Test Case IDs are unique (start from TC{i*100+1:03d})."
                    
                    chunk_result = self.llm.invoke(chunk_prompt)
                    chunk_content = chunk_result.content if hasattr(chunk_result, 'content') else str(chunk_result)
                    all_results.append(f"\n=== Document Section {i+1} Test Cases ===\n{chunk_content}")
                
                # Combine all results
                combined_result = "\n".join(all_results)
                
                # Add summary
                summary_prompt = f"""
Based on the following test cases generated from different sections of a document, provide a summary including:
1. Total number of test cases generated
2. Test cases by category (Frontend/Backend/Integration/API/Database)
3. Test cases by priority (High/Medium/Low)
4. Key testing areas covered
5. Any recommendations for additional testing

Test Cases:
{combined_result}
"""
                summary_result = self.llm.invoke(summary_prompt)
                summary_content = summary_result.content if hasattr(summary_result, 'content') else str(summary_result)
                
                return f"{combined_result}\n\n=== SUMMARY ===\n{summary_content}"
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating test cases: {str(e)}")

    def run(self, user_stories_text: str) -> str:
        """Fallback method for text input (maintains compatibility)"""
        prompt = self.prompt_template.format(document_content=user_stories_text)
        result = self.llm.invoke(prompt)
        return result.content if hasattr(result, 'content') else str(result)
