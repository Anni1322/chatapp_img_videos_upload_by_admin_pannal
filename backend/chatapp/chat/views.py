# from django.shortcuts import render

# # Create your views here.
# from django.http import JsonResponse
# from .ollama_service import generate_response
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
# def chat_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_input = data.get('message')
#         if user_input:
#             ai_response = generate_response(user_input)
#             return JsonResponse({'response': ai_response})
#         return JsonResponse({'error': 'No message provided'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from asgiref.sync import sync_to_async

# for excel sheet read
import pandas as pd
import os
# for excel sheet read

# for train input 
import re
from difflib import SequenceMatcher
# for train input 




# for respos add question
from rest_framework.views import APIView
from .serializers import ChatModelSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from .models import ChatModel
from django.core.files.uploadedfile import InMemoryUploadedFile
from .serializers import ChatModelSerializer 
# for respos add question



# @csrf_exempt
# def chat_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_input = data.get('message')
#         if user_input:
#             ai_response = generate_response(user_input)
#             return JsonResponse({'response': ai_response})  # Return the full response
#         return JsonResponse({'error': 'No message provided'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)


# @csrf_exempt
# def chat_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_input = data.get('message')
#         if user_input:
#             ai_response, response_time = generate_response(user_input)
#             return JsonResponse({
#                 'response': ai_response,
#                 'response_time': response_time  # Include the response time in the JSON response
#             })
#         return JsonResponse({'error': 'No message provided'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)




# @csrf_exempt
# async def chat_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_input = data.get('message')
#         if user_input:
#             ai_response = await generate_response(user_input)
#             return JsonResponse({'response': ai_response[0]})
#         return JsonResponse({'error': 'No message provided'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)





# for excel sheet read
# Get the base directory of your project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load_excel_data():
    # Construct the file path
    file_path = os.path.join(BASE_DIR, 'chat', 'dataset', 'answers.xlsx')    
    try:
        # Load the Excel file
        df = pd.read_excel(file_path)
        print("Excel Data Loaded Successfully.")
        print(df)  # Print the entire DataFrame content to the console
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
# Load data and print it to the console
excel_data = load_excel_data()
# for excel sheet read


# for save 
# Save updated data back to the Excel sheet
def save_excel_data(df):
    file_path = os.path.join(BASE_DIR, 'chat', 'dataset', 'answers.xlsx')
    df.to_excel(file_path, index=False)
# for save 


# Function to search for the response in the Excel sheet
def search_response(user_input, excel_data):
    # Normalize the user input to lowercase and tokenize (split into words)
    user_input_tokens = set(user_input.lower().split())
    
    for _, row in excel_data.iterrows():
        stored_message = row['message']

        # Check if stored_message is a string and normalize it
        if isinstance(stored_message, str):
            stored_message_tokens = set(stored_message.lower().split())

            # Check if all user input tokens are in the stored message tokens
            if user_input_tokens.issubset(stored_message_tokens):
                return row  # Return the entire row if a match is found

    return None  # Return None if no match is found


@csrf_exempt
async def chat_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message')
        print(user_input)

        if user_input:
            # Load the Excel data
            excel_data = load_excel_data()
            if excel_data is not None:
                # Search for a response in the Excel sheet
                response_from_excel = search_response(user_input, excel_data)
                
                if response_from_excel is not None:  # Check if the response is not None
                    return JsonResponse({
                        'user_message': user_input,  # The original user message
                        'answers': response_from_excel['answer'],  # The found answer from the Excel sheet
                        'image_path': response_from_excel.get('image_path', '') or '',  # Default to empty string if NaN
                        'video_path': response_from_excel.get('video_path', '') or '' 
                    })
        return JsonResponse({'error': 'No message provided'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)














# class ChatModelCreateView(APIView):
#     def post(self, request):
#         serializer = ChatModelSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()  # This will now handle base64-encoded media
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ChatModelCreateView(APIView):
    def post(self, request):
        # Load the Excel data
        excel_data = load_excel_data()
        # If no response is found in the Excel sheet, proceed with the original logic
        serializer = ChatModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This will now handle base64-encoded media
            
            # Load existing data
            df = load_excel_data()
            print(df)
            if df is not None:
                # Create a new DataFrame for the new row with correct column headers
                new_row = pd.DataFrame({
                    'message': [serializer.data['user_message']],  # Adjusting the column name to match your headers
                    'answer': [serializer.data['answers']],  # Adjusting the column name to match your headers
                    'image_path': [serializer.data.get('image_path', '')],  # Correctly mapping to the headers
                    'video_path': [serializer.data.get('video_path', '')]   # Ensure this column is included if needed
                })
                
                # Append the new row to the existing DataFrame
                updated_excel_data = pd.concat([df, new_row], ignore_index=True)  # Use pd.concat
                
                # Save the updated DataFrame back to the Excel file
                save_excel_data(updated_excel_data)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    




# List and Create ChatModel entries
class ChatModelListCreateView(APIView):
    def get(self, request):
        chats = ChatModel.objects.all()
        serializer = ChatModelSerializer(chats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChatModelSerializer(data=request.data)
        if serializer.is_valid():
            chat_model_instance = serializer.save()  # Save the ChatModel instance

            # Handle media uploads
            media_files = request.FILES.getlist('media')  # Retrieve the list of media files
            for media_file in media_files:
                # Check file type
                if media_file.content_type.startswith('image/'):
                    ChatMedia.objects.create(chat=chat_model_instance, image=media_file)
                elif media_file.content_type.startswith('video/'):
                    ChatMedia.objects.create(chat=chat_model_instance, video=media_file)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)