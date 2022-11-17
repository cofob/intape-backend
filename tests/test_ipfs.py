"""IPFS tests."""

from os import environ, path

import pytest
from asyncipfscluster import IPFSClient

client = IPFSClient(environ["IPFS_URL"])

# CID's can vary depending on the IPFS settings, so we can't hardcode them
# Because of this, the tests can fail if the IPFS settings are non-default
# (e.g. if block size is changed from 256kb to 1mb)
#
# To fix this, we can check file contents instead of CID's
# But local IPFS node may not have connectivity to the internet, or the
# peering with ipfs.io may not be established, so we can't use the
# ipfs.io gateway to check file contents.


@pytest.mark.asyncio
async def test_add_bytes() -> None:
    async with client as session:
        # Add a raw bytes with "text/plain" content type
        cid = await session.add_bytes(b"test", "text/plain")
        assert cid == "QmRf22bZar3WKmojipms22PkXH1MZGmvsqzQtuSvQE3uhm"


@pytest.mark.asyncio
async def test_add_file() -> None:
    async with client as session:
        # We use a file that is statically included in the repo
        # and we know the CID of this file, so we can hardcode it
        cid = await session.add_file(path.join("tests", "dummy.txt"), "text/plain")
        assert cid == "QmRJaHfsTiD5JfhGju8EUKATgKYPn4jgexTipVLCTKEg6j"


@pytest.mark.asyncio
async def test_remove_cid() -> None:
    async with client as session:
        # Remove a CID that we know exists (dummy.txt)
        await session.remove("QmRJaHfsTiD5JfhGju8EUKATgKYPn4jgexTipVLCTKEg6j")
        # Remove a CID that we know doesn't exist
        await session.remove("bafybeidlkbnqjddmsowjmbvrfrt7b54qqjxwrlmtvmdfpah5qqo72rvxvm")
