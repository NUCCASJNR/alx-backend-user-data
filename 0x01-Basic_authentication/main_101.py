#!/usr/bin/env python3

from api.v1.auth.auth import Auth

auth = Auth()
path_to_check = "/api/v1/stats"
excluded_paths = ["/api/v1/stat*", "/api/v1/stats/"]

# Both of these will return False
result1 = auth.require_auth(path_to_check, excluded_paths)
print(result1)  # False

path_to_check2 = "/api/v1/stats/"
result2 = auth.require_auth(path_to_check2, excluded_paths)
print(result2)  # False

check = "/api/v1/users"

res = auth.require_auth(check, ["/api/v1/us*"])
print(res)
