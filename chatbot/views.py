from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
import json
from .models import ChatSession, ChatMessage
from .ai_brain import process_message


def chatbot_page(request):
    # Create or get session
    if 'chat_session_id' not in request.session:
        request.session['chat_session_id'] = str(uuid.uuid4())

    session_id = request.session['chat_session_id']
    chat_session, created = ChatSession.objects.get_or_create(session_id=session_id)

    # Get chat history
    messages = ChatMessage.objects.filter(session=chat_session).order_by('created_at')

    return render(request, 'chatbot/chat.html', {
        'messages': messages,
        'session': chat_session,
    })


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            if not user_message:
                return JsonResponse({'error': 'Empty message'}, status=400)

            # Get session
            session_id = request.session.get('chat_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['chat_session_id'] = session_id

            chat_session, _ = ChatSession.objects.get_or_create(session_id=session_id)

            # Save user message
            ChatMessage.objects.create(
                session=chat_session,
                is_user=True,
                message=user_message
            )

            # Get bot response
            bot_response = process_message(chat_session, user_message)

            # Save bot response
            ChatMessage.objects.create(
                session=chat_session,
                is_user=False,
                message=bot_response
            )

            return JsonResponse({
                'response': bot_response,
                'step': chat_session.step
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
