from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class RegistrationThrottle(AnonRateThrottle):
    rate = '20/hour'


class TokenObtainThrottle(AnonRateThrottle):
    rate = '30/hour'


class TokenRefreshThrottle(UserRateThrottle):
    rate = '7/hour'


class GeneralThrottle(UserRateThrottle):
    rate = '30/minute'