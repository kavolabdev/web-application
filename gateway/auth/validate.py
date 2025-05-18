import os, requests

AUTH_SVC = "http://auth:5000" #os.environ.get("AUTH_SVC_ADDRESS")

def token(request):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        return None, ("missing credentials", 401)

    try:
        response = requests.post(
            f"{AUTH_SVC}/validate",
            headers={"Authorization": auth_header}
        )
    except requests.exceptions.RequestException as e:
        return None, (f"auth service unreachable: {str(e)}", 503)

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)