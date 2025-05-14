package com.hnu.muwu.service;

import com.hnu.muwu.bean.MyFile;

public interface FileService {

    int insertFile(MyFile file);

    Boolean fileOperatorExtend(String filePath, String type);

}
