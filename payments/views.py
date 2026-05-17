import logging
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  # Required for 401 error
from django.core.cache import cache 
from .encryption_utils import encrypt_data, decrypt_data  # Added decrypt for testing

# Part D: Secure Logging
logger = logging.getLogger('django')

class UserRegistrationView(APIView):
    # No permission_classes here so new users can actually register
    def post(self, request):
        # Part C: Manual Rate Limiting
        ip = request.META.get('REMOTE_ADDR')
        cache_key = f"rl_{ip}"
        attempts = cache.get(cache_key, 0)

        if attempts >= 5: 
            logger.warning(f"Rate limit exceeded for IP: {ip}")
            return Response(
                {"error": "Too many requests. Try again later."}, 
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        cache.set(cache_key, attempts + 1, 60)
        logger.warning(f"Registration attempt {attempts + 1} from IP: {ip}")
        return Response({"message": "Registration endpoint reachable!"})

class SecurePaymentView(APIView):
    # --- Part E: Access without authentication ---
    # This line triggers the 401 error if No Auth is selected in Postman
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        card_no = request.data.get('card_number')
        
        # --- Part E: Invalid encrypted payloads ---
        # Logic to check if we are receiving data that needs decryption
        action = request.data.get('action')
        if action == "decrypt":
            try:
                decrypted_val = decrypt_data(card_no)
                return Response({"decrypted": decrypted_val})
            except Exception as e:
                logger.error(f"Decryption failed: {str(e)}")
                return Response({"error": "Invalid encrypted payload"}, status=status.HTTP_400_BAD_REQUEST)

        if not card_no:
            logger.warning("Payment attempt with missing data")
            return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Part B: Encrypt sensitive data
        encrypted_card = encrypt_data(card_no)
        
        logger.warning(f"Secure payment processed. Data encrypted.")
        return Response({
            "status": "Encrypted and Stored", 
            "encrypted_payload": encrypted_card
        })