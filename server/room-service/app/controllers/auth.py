import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Dict
import os

# It's better to use an environment variable for the auth service URL
# Ensure this URL points to your auth-service instance
AUTH_SERVICE_BASE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:5000")

# The tokenUrl should ideally point to the actual token endpoint of the auth-service.
# This is used by Swagger UI for interactive authentication.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{AUTH_SERVICE_BASE_URL}/token", auto_error=False
)


async def get_current_user_payload(
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> Dict:
    if token is None:
        # This case handles when the token is not provided at all.
        # OAuth2PasswordBearer with auto_error=False returns None if token is not found.
        # If auto_error=True (default), FastAPI would automatically return a 401.
        # We make it explicit here for clarity or custom handling if needed.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    async with httpx.AsyncClient() as client:
        try:
            verify_url = f"{AUTH_SERVICE_BASE_URL}/verify-token/{token}"
            response = await client.get(verify_url)

            if response.status_code == 200:
                # Assuming the auth-service returns the token payload (e.g., user details)
                # upon successful verification. If it only returns a confirmation message,
                # this will be that message.
                return response.json()
            elif response.status_code == 401:  # Explicitly handle 401 from auth service
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: Verification failed by auth service",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                # Handle other unexpected errors from auth_service
                # Log response.text for debugging if necessary
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Authentication service error: {response.status_code}",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except httpx.RequestError as exc:
            # Network errors or auth service is down
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not connect to authentication service: {str(exc)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:  # Catch any other unexpected errors during the process
            # Log the error e for debugging
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred during token verification: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )


# Convenience dependency if you just need to ensure the user is authenticated
# and don't need the payload directly in the route function signature.
# You can still access it via other means if needed, or just rely on it raising errors.
async def ensure_authenticated(
    payload: Annotated[Dict, Depends(get_current_user_payload)],
):
    # This dependency doesn't return anything but ensures get_current_user_payload runs
    # and raises an exception if authentication fails.
    return payload
