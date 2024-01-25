# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from pymongo import MongoClient
# import PyPDF2
# import re

# app = Flask(__name__)
# CORS(app, supports_credentials=True, origins="http://localhost:3000")

# # Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/')
# db = client['your_database_name']  # Replace 'your_database_name' with your desired database name
# job_listings_collection = db['job_listings']

# def extract_text_from_pdf(file):
#     text = ''
#     pdf_reader = PyPDF2.PdfReader(file)
#     for page_num in range(len(pdf_reader.pages)):
#         page = pdf_reader.pages[page_num]
#         text += page.extract_text()
#     return text
    
# @app.route('/upload', methods=['POST'])
# def upload_resume():
#     if 'resume' not in request.files:
#         return jsonify({'error': 'No file part'})

#     resume_file = request.files['resume']

#     if resume_file.filename == '':
#         return jsonify({'error': 'No selected file'})

#     try:
#         pdf_text = extract_text_from_pdf(resume_file)
#         return jsonify({'pdfText': pdf_text})
#     except Exception as e:
#         return jsonify({'error': str(e)})



# # def filter_jobs_by_skills(job_listing, skills):
# #     job_description = job_listing['description']
# #     for skill in skills:
# #         if re.search(rf'\b{re.escape(skill)}\b', job_description, re.IGNORECASE):
# #             return True
# #     return False

# @app.route('/add_job', methods=['POST'])
# def add_job_listing():
#     data = request.json
#     title = data.get('title')
#     skills = data.get('skills')
#     location = data.get('location')

#     if not title or not skills or not location:
#         return jsonify({'error': 'Incomplete data'})

#     job_listing = {
#         'title': title,
#         'skills': skills,
#         'location': location
#     }

#     result = job_listings_collection.insert_one(job_listing)
#     return jsonify({'job_id': str(result.inserted_id)})

# # @app.route('/get_jobs', methods=['GET'])
# # def get_job_listings():
# #     # Extract skills from resume
# #     resume_skills = extract_text_from_pdf(request.files['resume']).split()

# #     # Retrieve all job listings from MongoDB
# #     all_job_listings = list(job_listings_collection.find({}, {'_id': 0}))

# #     # Filter job listings based on skills
# #     filtered_job_listings = [job for job in all_job_listings if filter_jobs_by_skills(job, resume_skills)]

# #     return jsonify({'job_listings': filtered_job_listings})
# # @app.route('/get_jobs', methods=['GET'])
# # def get_job_listings():
# #     job_listings = list(job_listings_collection.find({}, {'_id': 0}))
# #     return jsonify({'job_listings': job_listings})
# @app.route('/get_jobs', methods=['GET'])
# def get_job_listings():
#     # Check if 'resumeSkills' parameter is present in the query parameters
#     resume_skills = request.args.get('resumeSkills', None)

#     # If resumeSkills is provided, filter jobs by skills
#     if resume_skills:
#         try:
#             resume_skills = resume_skills.split()  # Convert space-separated skills into a list
#             # Retrieve all job listings from MongoDB
#             all_job_listings = list(job_listings_collection.find({}, {'_id': 0}))

#             # Filter job listings based on skills
#             filtered_job_listings = [job for job in all_job_listings if filter_jobs_by_skills(job, resume_skills)]

#             return jsonify({'job_listings': filtered_job_listings})
#         except Exception as e:
#             return jsonify({'error': str(e)})
#     else:
#         # If resumeSkills is not provided, return all job listings
#         job_listings = list(job_listings_collection.find({}, {'_id': 0}))
#         return jsonify({'job_listings': job_listings})
# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import PyPDF2
import re
import pytesseract
from PIL import Image
import spacy
app = Flask(__name__)
CORS(app, supports_credentials=True, origins="http://localhost:3000")

# Load the English model for spaCy
nlp = spacy.load('en_core_web_sm')

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']  # Replace 'your_database_name' with your desired database name
job_listings_collection = db['job_listings']

def extract_text_from_pdf(file):
    text = ''
    pdf_reader = PyPDF2.PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'})

    resume_file = request.files['resume']

    if resume_file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        pdf_text = extract_text_from_pdf(resume_file)
        return jsonify({'pdfText': pdf_text})
    except Exception as e:
        return jsonify({'error': str(e)})

def filter_jobs_by_skills(job_listing, skills):
    job_description = job_listing['description']
    for skill in skills:
        if re.search(rf'\b{re.escape(skill)}\b', job_description, re.IGNORECASE):
            return True
    return False

@app.route('/add_job', methods=['POST'])
def add_job_listing():
    data = request.json
    title = data.get('title')
    skills = data.get('skills')
    location = data.get('location')

    if not title or not skills or not location:
        return jsonify({'error': 'Incomplete data'})

    job_listing = {
        'title': title,
        'skills': skills,
        'location': location
    }

    result = job_listings_collection.insert_one(job_listing)
    return jsonify({'job_id': str(result.inserted_id)})

@app.route('/get_jobs', methods=['GET'])
def get_job_listings():
    # Check if 'resumeSkills' parameter is present in the query parameters
    resume_skills = request.args.get('resumeSkills', None)

    # If resumeSkills is provided, filter jobs by skills
    if resume_skills:
        try:
            resume_skills = resume_skills.split()  # Convert space-separated skills into a list
            # Retrieve all job listings from MongoDB
            all_job_listings = list(job_listings_collection.find({}, {'_id': 0}))

            # Filter job listings based on skills
            filtered_job_listings = [job for job in all_job_listings if filter_jobs_by_skills(job, resume_skills)]

            return jsonify({'job_listings': filtered_job_listings})
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        # If resumeSkills is not provided, return all job listings
        job_listings = list(job_listings_collection.find({}, {'_id': 0}))
        return jsonify({'job_listings': job_listings})

if __name__ == '__main__':
    app.run(debug=True)



