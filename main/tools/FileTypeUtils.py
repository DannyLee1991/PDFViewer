import filetype


def is_pdf(file_path):
    """
    判断文件是否为pdf
    :param file_path:
    :return:
    """
    r = filetype.guess_mime(file_path)
    return r == 'application/pdf'
