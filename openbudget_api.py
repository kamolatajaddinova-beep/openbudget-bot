import aiohttp

SEND_SMS_URL = "https://openbudget.uz/api/v1/user/temp/vote/send-code"
VERIFY_CODE_URL = "https://openbudget.uz/api/v1/user/temp/vote/verify-code"

async def send_openbudget_sms(phone: str, initiative_id: str):
    async with aiohttp.ClientSession() as session:
        payload = {"phone": phone, "initiative_id": initiative_id}
        try:
            async with session.post(SEND_SMS_URL, json=payload, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {"success": True, "session_id": data.get("session_id")}
                return {"success": False, "message": "SMS yuborishda xatolik."}
        except Exception as e:
            return {"success": False, "message": str(e)}

async def verify_openbudget_code(session_id: str, code: str):
    async with aiohttp.ClientSession() as session:
        payload = {"session_id": session_id, "code": code}
        try:
            async with session.post(VERIFY_CODE_URL, json=payload, timeout=10) as resp:
                if resp.status == 200:
                    return {"success": True}
                return {"success": False, "message": "SMS kod noto'g'ri."}
        except Exception as e:
            return {"success": False, "message": str(e)}
