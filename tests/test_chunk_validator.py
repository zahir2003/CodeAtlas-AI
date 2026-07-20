from app.validation.chunk_validator import ChunkValidator


def test_empty_chunk():

    chunks = []

    assert ChunkValidator.validate(chunks) == []