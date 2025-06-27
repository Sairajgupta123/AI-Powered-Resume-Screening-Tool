import tempfile

with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
    tmp_file.write(up_file.getbuffer())
    tmp_path = tmp_file.name
