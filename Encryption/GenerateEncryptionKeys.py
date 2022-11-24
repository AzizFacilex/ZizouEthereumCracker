import rsa

# generate public and private keys with
# rsa.newkeys method,this method accepts
# key length as its parameter
publicKey, privateKey = rsa.newkeys(1024)
print("PUBLIC_KEY: " + str(publicKey))
print("PRIVATE_KEY: " + str(privateKey))
