"""Eth crypto utils."""
from logging import getLogger

from Crypto.Hash import keccak
from eth_account import Account
from eth_account.messages import encode_defunct

log = getLogger(__name__)


def verify_signature(message: str, signature: str, address: str) -> bool:
    r"""Verify signature.

    Args:
        message (str): message
        signature (str): signature
        address (str): address

    Examples:
        >>> message = "Sign this message to login to the site.\nThis doesn't cost you anything and is free of any gas fees.\n\nNonce: 858511d00a8390c036e62290d7c3d7b51e40372d53109fe416975b468c6a9ea4"  # noqa: E501
        >>> signature = "0xe66a92996cd08aaca46cb1c605f8a41f88945c2921eec8f2d03b342c41816de17f945332e829afde6171006268bfa31d324c799583e59dc1c1322beee1f7b8651b"  # noqa: E501
        >>> address = "0x2302a71cb0e286e0f930ee47fdcd9bf82bac05dd"
        >>> verify_signature(message, signature, address)
        True

    Returns:
        bool: True if signature is valid, False otherwise
    """
    try:
        message_hash = encode_defunct(text=message)
        return Account.recover_message(message_hash, signature=signature).lower() == address.lower()
    except Exception as e:
        log.exception("Error while verifying signature: %s", e)
        return False


def verify_signature_eth_sign(message: str, signature: str, address: str) -> bool:
    """Verify signature.

    Args:
        message (str): message
        signature (str): signature
        address (str): address

    Returns:
        bool: True if signature is valid, False otherwise
    """
    try:
        message_hash = keccak.new(digest_bits=256)
        message_hash.update(message.encode("utf-8"))
        return Account.recover_message(message_hash, signature=signature).lower() == address.lower()
    except Exception as e:
        log.exception("Error while verifying signature: %s", e)
        return False
