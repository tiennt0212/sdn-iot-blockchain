#!/usr/bin/env python3
import tokenlib

token=tokenlib.make_token(
    {
        "deviceId":12,
    },
    secret="OCEANSONG"
)

print("Token is: \n\t{}\n".format(token))

data=tokenlib.parse_token(
    token,
    secret="OCEANSONG"
)
print("Data parse from token is:\n\t{}\n".format(data))

# dataFuture=tokenlib.parse_token(
#     token,
#     secret="OCEANSONG",
#     now=12345678999
# )#Token has expired
# print("Data parse from token is:\n\t{}\n".format(dataFuture))
