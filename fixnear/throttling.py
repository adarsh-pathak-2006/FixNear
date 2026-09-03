from rest_framework.throttling import UserRateThrottle

class RegistrationThrottle(UserRateThrottle):
    rate="20/hour"

class TokenObtainThrottle(UserRateThrottle):
    rate="30/hour"

class TokenRefreshThrottle(UserRateThrottle):
    rate="7/hour"

class GeneralThrottle(UserRateThrottle):
    rate="30/minute"