def byte_to_srt(bytes: int) -> str:
    if bytes < 1024:
        return f'{bytes} B'
    elif bytes < 1024 * 1024:
        return f'{bytes / 1024:.2f} KB'
    else:
        return f'{bytes / 1024 / 1024:.2f} MB'