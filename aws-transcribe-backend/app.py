from flask import Flask, request, jsonify, render_template
import boto3
import uuid
import os

app = Flask(__name__)

# AWS S3 and Transcribe setup
AWS_REGION = "us-east-1"  # Change this to your AWS region
S3_BUCKET = "bucket-name"  # Change to your S3 bucket name
TRANSCRIBE_ROLE_ARN = "arn:aws:iam::0000000:abcd/abcd"  # ARN for your Transcribe IAM role

s3_client = boto3.client('s3', region_name=AWS_REGION)
transcribe_client = boto3.client('transcribe', region_name=AWS_REGION)

# Route for the home page (root URL)
@app.route('/')
def home():
    return render_template('index.html')

# Function to upload files to S3
def upload_to_s3(file, filename):
    s3_client.upload_fileobj(file, S3_BUCKET, filename)
    return f"s3://{S3_BUCKET}/{filename}"

# Function to start transcription job
def start_transcription_job(s3_uri, job_name):
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': s3_uri},
        MediaFormat='mp3',
        LanguageCode='en-US',
        OutputBucketName=S3_BUCKET
    )
    return response

# Upload route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = f"{uuid.uuid4()}.mp3"  # Create a unique filename for the uploaded file
    s3_uri = upload_to_s3(file, filename)
    job_name = f"transcription-{uuid.uuid4()}"  # Create a unique job name for transcription

    try:
        start_transcription_job(s3_uri, job_name)
        return jsonify({'message': 'File uploaded and transcription started', 'job_name': job_name}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to check the transcription job status
@app.route('/transcription/<job_name>', methods=['GET'])
def get_transcription(job_name):
    try:
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        if response['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            return jsonify({'status': 'COMPLETED', 'transcript_uri': transcript_uri})
        elif response['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
            return jsonify({'status': 'FAILED'}), 500
        else:
            return jsonify({'status': 'IN_PROGRESS'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True)