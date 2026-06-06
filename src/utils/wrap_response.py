def success_response(data, message="success", status=200 ,error=False):
    return {"status": status, "message": message, "data": data, "error": error}


def list_response(list, offset, limit, total, message="success", status=200 ,error=False):
    return {
        "status": status,
        "message": message,
        "data": list,
        "pagination": {
            "offset": offset,
            "limit": limit,
            "total": total,
        },
        "error": error,
    }
