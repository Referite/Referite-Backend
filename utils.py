def error_handler(f):
    async def wrapper(*arg, **kwargs):
        try:
            return await f(*arg, **kwargs)
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    return wrapper