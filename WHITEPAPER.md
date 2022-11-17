# API reference

InTape draft API reference.

## Authorization 🔑

Authorization used only for petya and vasya users, it is not intended for metamask users.

For metamask user we perform captcha validation for anti-spam purposes.
Vasya-users gets verificated in registration step.

Access token contains basic user information: username (optional), email (optional), address (wallet address).
Refresh token id stored in database.

 - POST `/oauth/register` (vasya)
   Register user.
   Returns: jwt token-pair. Access token + Refresh token.
 - POST `/oauth/login` (vasya)
   Login user.
   Returns: jwt token-pair. Access token + Refresh token.
 - POST `/oauth/rotate-token` (vasya)
   Accepts refresh token and issues new access token.
 - POST `/captcha/<REPLACEME>` (metamask on register)
   Only for metamask users.
   Accepts: captcha answer.
   Returns: access token with increased lifetime.

```python

User: (only vasyas)
    id: int
    address: str
    private_key: str
    email: Optional[str]
    username: Optional[str]
```


## Storage (IPFS) 💦

 - POST  `/storage/upload`
   Upload media file to IPFS cluster wwith max replication set to 1. Stored for hour.
   After an hour, if no NFT has been created, we remove the file from the cluster.
   If NFT is created, we increase the number of replication.
   Returns: IPFS CID.

```python
NftFile:
    cid: str
    nft: address
    created_at: timestamp

ChatFile:
    cid: str
    dialog: int (FK[dialog.id])
    created_at: timestamp
```


## Blockchain 🖼

 - POST `/blockchain/nft`
   Create NFT item. Accepts `collection_id`.
 - POST `/blockchain/collection`
   Create NFT collection.
   Returns: access token.


## PM

Ways to solve the problem
 - E2EE
 - Storing plain text in a database

### E2EE

The clients set up a symmetric encryption key via the Diffie-Hellman protocol, then they can start sending each other messages. We store their key exchange process in the database and return it when prompted for history (this is necessary for offline messages and correspondence history).

This approach has several disadvantages, one of them is that we can't send a message to an account before we deduce the shared key.

 - GET  `/chat/`
   Get list of active dialogs (recipient addresses and read status).
 - POST `/chat/send`
   Message must be encrypted with recipient public key.
   Accepts `address` (unique id) and `text`.
 - GET  `/chat/history`
   Messages are encrypted with public key and can be encrypted by private key.
   Accepts `address` (unique id), limit, offset.

### Plain-text

We store all messages in plain text. The easiest option to implement. It is necessary to notify the user that the messages are not encrypted and are stored on the server.

 - GET  `/chat/`
   Get list of active dialogs (recipient addresses and read status).
 - POST `/chat/send`
   Accepts `address` (unique id) and `text`.
 - GET  `/chat/history`
   Accepts `address` (unique id), limit, offset.

# Models

```python
Dialog:
    id: int
    address_1: address
    address_2: address
    last_read_1: message.id
    last_read_2: message.id

Message:
    id: int
    sent_at: timestamp
    from: address
    dialog_id: int
    text: Optional[text]
    attachments: List[CID] // Only media types (photo | video | audio).
```


## Comments & Likes

We have two ways of solving the problem:
 - Server-side storage
 - Storage in a separate blockchain with a key-value table and low write price (e.g. (Emercoin)[https://emercoin.com/])

### Server-side storage

Just store in DB.

```python
Post:
    id: int
    address: str (nft address)

Like:
    post_id: int (FK[post.id])
    user_address: int (FK[user.address])
    PK(post_id, user_address)
```

### Storage in a separate blockchain

Benefits:
 - True decentralization.

Problems:
 - There is no way to regulate spam.
 - Although blockchain transactions are cheap, they come at a higher price than just storing them in a database.
