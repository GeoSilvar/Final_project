import requests
import base64
from datetime import datetime
import logging
from typing import Optional, Dict
from ..config import settings

logger = logging.getLogger(__name__)

class MpesaService:
    def __init__(self):
        self.access_token = None
        self.token_expiry = None
    
    def get_access_token(self) -> Optional[str]:
        """Get M-Pesa API access token"""
        try:
            consumer_key = settings.MPESA_CONSUMER_KEY
            consumer_secret = settings.MPESA_CONSUMER_SECRET
            credentials = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()
            
            response = requests.get(
                "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
                headers={"Authorization": f"Basic {credentials}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data['access_token']
                self.token_expiry = datetime.now().timestamp() + data['expires_in']
                return self.access_token
            else:
                logger.error(f"Failed to get access token: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting access token: {e}")
            return None
    
    def initiate_stk_push(self, phone_number: str, amount: float, account_ref: str) -> Dict:
        """Initiate STK push for fee payment"""
        try:
            token = self.get_access_token()
            if not token:
                return {"success": False, "error": "Failed to get access token"}
            
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            password = base64.b64encode(
                f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode()
            ).decode()
            
            payload = {
                "BusinessShortCode": settings.MPESA_SHORTCODE,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": settings.MPESA_SHORTCODE,
                "PhoneNumber": phone_number,
                "CallBackURL": f"{settings.BASE_URL}/api/v1/fees/mpesa-callback",
                "AccountReference": account_ref,
                "TransactionDesc": "School Fees Payment"
            }
            
            response = requests.post(
                "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {"success": True, "data": data}
            else:
                logger.error(f"STK push failed: {response.text}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            logger.error(f"Error initiating STK push: {e}")
            return {"success": False, "error": str(e)}