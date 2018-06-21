from pgbackup import storage
import tempfile
import pytest

infile = tempfile.TemporaryFile()
infile.write(b"testing")
infile.seek(0)

outfile = tempfile.NamedTemporaryFile(delete=False)

def test_local_storage():

    storage.local(infile, outfile)

    with open(outfile.name, 'rb') as f:
        assert f.read() ==  b"testing"

def test_s3_storage(mocker):

    client = mocker.Mock()

    storage.s3(client, infile, "bucket", "filename")

    client.upload_fileobj.assert_called_with(infile, "bucket", "filename")
