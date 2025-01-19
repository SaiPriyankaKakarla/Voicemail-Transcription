# Voicemail Transcription App

## Description

The **Voicemail Transcription App** allows users to upload audio files (e.g., MP3 voicemails) and transcribe them using **AWS Transcribe**. The application provides a simple web interface for uploading files, and it triggers an AWS transcription job that processes the audio and returns the transcribed text as a downloadable JSON file.

### Features:
- Upload voicemail audio files.
- Automatically start transcription jobs using AWS Transcribe.
- Retrieve and view transcription results as JSON.
- Integration with AWS S3 for storing audio files and transcription results.

## Demo Video

[Watch the demo video here](https://www.youtube.com/your-video-link) to see the application in action!

## Requirements

### AWS Configuration:
- **AWS account**: You’ll need an AWS account with permissions to use Amazon S3 and Amazon Transcribe.
- **IAM User**: Create an IAM user with access to S3 and Transcribe services. Make sure to attach the necessary permissions to the IAM user.
- **S3 Bucket**: Set up an S3 bucket for storing uploaded audio files and transcription results.

### Local Setup:
- **Python 3.8+**
- **Flask** for the backend
- **boto3** for AWS SDK
- **HTML/CSS** for the frontend

