import zh2autosdpro
import questionary

file_path = '/Users/ruanliqing/Library/Mobile Documents/com~apple~CloudDocs/startup/推文/小说集/最后的真相.docx'

sentences = zh2autosdpro.extract_sentences_from_docx_zh(file_path)