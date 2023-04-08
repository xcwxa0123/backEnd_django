KAKUYOMU_PARAMS = {
    'TARGET_DOM_CLASS': 'js-episode-body', # 目标TEXT所在DOM的class
    'WRITE_DIR_NAME': 'kakuyomu_transed', # 要写入的文件夹（没有会创建）
    'TARGET_CREATE_PATH': './', # WRITE_DIR_NAME所在地址
    'TEXTFILE_PATH': 'kakuyomu_file' # 扒下来的HTML文件所在文件夹
}

SHOUSETSUNAROU_PARAMS = {
    'TARGET_DOM_CLASS': 'novel_view', # 目标TEXT所在DOM的class
    'WRITE_DIR_NAME': 'shousenarou_transed', # 要写入的文件夹（没有会创建）
    'TARGET_CREATE_PATH': './', # WRITE_DIR_NAME所在地址
    'TEXTFILE_PATH': 'shousenarou_file', # 扒下来的HTML文件所在文件夹
    'CHAPTER_NUM_CLASS': 'novel_subtitle', # 标题中没有章号的情况下去文件里取
    'CHAPTER_NUM_DOM_TYPE' : 'div' # 包含章节号的DOM类型
}