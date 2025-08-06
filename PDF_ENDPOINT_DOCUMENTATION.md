# PDF Test Case Generation Endpoint

## Overview
The PDF Test Case Generation endpoint allows users to upload PDF documents containing requirements, specifications, or user stories and automatically generate comprehensive test cases using AI.

## Endpoint Details

### URL
```
POST /test-cases/pdf
```

### Content Type
```
multipart/form-data
```

### Parameters

#### Required Parameters
- **file** (file): PDF file containing requirements or specifications
  - Format: PDF only
  - Max size: 20MB
  - Must contain readable text content

#### Optional Parameters
- **test_category** (string): Filter test cases by category
  - Options: `All`, `Frontend`, `Backend`, `Integration`, `API`, `Database`
  - Default: `All`

- **priority_filter** (string): Filter test cases by priority
  - Options: `All`, `High`, `Medium`, `Low`
  - Default: `All`

## Request Example

### Using curl
```bash
curl -X POST "http://localhost:8000/test-cases/pdf" \
  -F "file=@requirements.pdf" \
  -F "test_category=Frontend" \
  -F "priority_filter=High"
```

### Using Python requests
```python
import requests

url = "http://localhost:8000/test-cases/pdf"
files = {'file': ('requirements.pdf', open('requirements.pdf', 'rb'), 'application/pdf')}
data = {
    'test_category': 'Frontend',
    'priority_filter': 'High'
}

response = requests.post(url, files=files, data=data)
result = response.json()
```

### Using JavaScript/Fetch
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('test_category', 'All');
formData.append('priority_filter', 'High');

fetch('/test-cases/pdf', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## Response Format

### Success Response (200 OK)
```json
{
  "test_cases": {
    "content": "### Test Cases\n\n#### User Registration\n\n**TC001: User Registration with valid data**\n- Test Category: Frontend\n- Priority: High\n...",
    "source": "PDF Document",
    "filename": "requirements.pdf",
    "filters": {
      "test_category": "Frontend",
      "priority_filter": "High"
    }
  }
}
```

### Error Responses

#### 400 Bad Request - Invalid File Type
```json
{
  "detail": "Only PDF files are allowed"
}
```

#### 400 Bad Request - File Too Large
```json
{
  "detail": "File size exceeds 20MB limit"
}
```

#### 400 Bad Request - Empty File
```json
{
  "detail": "Empty file uploaded"
}
```

#### 400 Bad Request - No Text Content
```json
{
  "detail": "No text content found in the PDF"
}
```

#### 422 Unprocessable Entity - Missing File
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "file"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

## Generated Test Case Format

The AI generates test cases in the following structured format:

```
### Test Cases

#### [Feature/Module Name]

**TC001: [Test Case Title]**
- Test Case ID: TC001
- Test Category: Frontend/Backend/Integration/API/Database
- Priority: High/Medium/Low
- Preconditions: [Required setup conditions]
- Test Steps:
    1. [Detailed step 1]
    2. [Detailed step 2]
    3. [Detailed step 3]
- Expected Results: [Expected outcome]
- Test Data Requirements: [Required test data]
- Post-conditions: [System state after test]
```

## Features

### 1. Comprehensive Test Coverage
- **Functional Testing**: Core feature validation
- **UI/UX Testing**: User interface and experience
- **API Testing**: Backend service validation
- **Database Testing**: Data integrity and operations
- **Integration Testing**: Component interaction
- **Negative Testing**: Error handling scenarios
- **Security Testing**: Authentication and authorization
- **Performance Testing**: Load and response time

### 2. Smart Document Processing
- **Text Extraction**: Uses PyMuPDF for accurate text extraction
- **Large Document Handling**: Automatically chunks large documents
- **Page-by-Page Processing**: Maintains document structure
- **Content Validation**: Ensures readable content exists

### 3. Filtering and Categorization
- **Category Filtering**: Focus on specific test types
- **Priority Filtering**: Emphasize critical test cases
- **Traceability**: Links test cases back to requirements

### 4. Advanced Features
- **Multi-page Support**: Handles documents of any length
- **Unique Test IDs**: Generates sequential test case identifiers
- **Summary Generation**: Provides overview for large documents
- **Error Handling**: Comprehensive validation and error reporting

## Best Practices

### 1. PDF Preparation
- Ensure PDF contains readable text (not just images)
- Use clear, structured requirements format
- Include acceptance criteria where possible
- Organize content by features or modules

### 2. Optimal File Size
- Keep files under 20MB for best performance
- For larger documents, consider splitting by feature
- Ensure good text quality for accurate extraction

### 3. Using Filters Effectively
- Use `Frontend` filter for UI-focused requirements
- Use `Backend` filter for API and business logic requirements
- Use `Integration` filter for system interaction requirements
- Use `High` priority filter for critical path testing

## Integration with Existing Workflow

### 1. Requirements Management
- Upload PRD documents directly
- Generate test cases from user story documents
- Process technical specification PDFs

### 2. Test Planning
- Use generated test cases as starting point
- Refine and customize based on project needs
- Integrate with existing test management tools

### 3. Quality Assurance
- Ensure comprehensive coverage of requirements
- Validate test case completeness
- Use for test estimation and planning

## Limitations

1. **PDF Format**: Only supports PDF files with extractable text
2. **File Size**: Maximum 20MB per upload
3. **Language**: Optimized for English content
4. **Image Content**: Cannot extract text from images within PDFs
5. **Complex Layouts**: May have issues with very complex PDF layouts

## Security Considerations

1. **File Validation**: Strict PDF format validation
2. **Size Limits**: Prevents resource exhaustion
3. **Content Scanning**: Validates file content before processing
4. **Temporary Storage**: Files are not permanently stored
5. **Error Handling**: Secure error messages without system exposure

## Performance

- **Small PDFs** (< 1MB): ~5-15 seconds processing time
- **Medium PDFs** (1-5MB): ~15-45 seconds processing time
- **Large PDFs** (5-20MB): ~45-120 seconds processing time

Processing time depends on:
- Document length and complexity
- Number of requirements
- OpenAI API response time
- System resources

## Troubleshooting

### Common Issues

1. **"No text content found"**
   - PDF may be image-based
   - Try OCR preprocessing
   - Ensure PDF has selectable text

2. **"File size exceeds limit"**
   - Compress PDF or split into smaller files
   - Remove unnecessary images or content

3. **Slow processing**
   - Large documents take longer
   - Consider using filters to reduce scope
   - Check network connectivity

4. **Incomplete test cases**
   - Ensure requirements are clearly written
   - Add more detail to source document
   - Try different filter combinations
