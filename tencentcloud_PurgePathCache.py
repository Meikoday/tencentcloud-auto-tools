# -*- coding: utf-8 -*-
import argparse
import hashlib
import hmac
import json
import sys
import time
from datetime import datetime

if sys.version_info[0] <= 2:
    from httplib import HTTPSConnection
else:
    from http.client import HTTPSConnection

def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def main():
    parser = argparse.ArgumentParser(description="腾讯云CDN刷新工具")
    parser.add_argument("-id", "--secret_id", required=True, help="腾讯云SecretId")
    parser.add_argument("-key", "--secret_key", required=True, help="腾讯云SecretKey")
    parser.add_argument("-r", "--region", default="", help="区域")
    parser.add_argument("-t", "--token", default="", help="Token")
    args = parser.parse_args()

    secret_id = args.secret_id
    secret_key = args.secret_key
    region = args.region
    token = args.token

    service = "cdn"
    host = "cdn.tencentcloudapi.com"
    version = "2018-06-06"
    action = "PurgePathCache"
    payload = "{\"Paths\":[\"https://www.meiko.ink/\"],\"FlushType\":\"flush\",\"UrlEncode\":false,\"Area\":\"mainland\"}"
    params = json.loads(payload)
    endpoint = "https://cdn.tencentcloudapi.com"
    algorithm = "TC3-HMAC-SHA256"
    timestamp = int(time.time())
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

    # ************* 步骤 1：拼接规范请求串 *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    canonical_headers = "content-type:%s\nhost:%s\nx-tc-action:%s\n" % (ct, host, action.lower())
    signed_headers = "content-type;host;x-tc-action"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" +
                         canonical_uri + "\n" +
                         canonical_querystring + "\n" +
                         canonical_headers + "\n" +
                         signed_headers + "\n" +
                         hashed_request_payload)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                      str(timestamp) + "\n" +
                      credential_scope + "\n" +
                      hashed_canonical_request)

    # ************* 步骤 3：计算签名 *************
    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (algorithm + " " +
                     "Credential=" + secret_id + "/" + credential_scope + ", " +
                     "SignedHeaders=" + signed_headers + ", " +
                     "Signature=" + signature)

    # ************* 步骤 5：构造并发起请求 *************
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json; charset=utf-8",
        "Host": host,
        "X-TC-Action": action,
        "X-TC-Timestamp": timestamp,
        "X-TC-Version": version
    }
    if region:
        headers["X-TC-Region"] = region
    if token:
        headers["X-TC-Token"] = token

    try:
        req = HTTPSConnection(host)
        req.request("POST", "/", headers=headers, body=payload.encode("utf-8"))
        resp = req.getresponse()
        print(resp.read().decode()) #解码输出，防止乱码
    except Exception as err:
        print(err)

if __name__ == "__main__":
    main()
